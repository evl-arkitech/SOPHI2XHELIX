# **Comprehensive Architecture and Security Framework for EVM Smart Contracts and Circular Reward Economies**

Modern smart contract engineering demands a precise reconciliation of low-level execution mechanics, formal defensive engineering, and mathematically consistent tokenomics. As the Ethereum Virtual Machine (EVM) ecosystem evolves through protocol upgrades such as the Dencun hard fork, architectural paradigms have shifted away from monolithic inheritance and ad-hoc storage structures toward isolated, transient, and namespaced computational frameworks1.

Protocols attempting to establish a circular economy that issues external yield—specifically in centralized, fiat-backed stablecoins such as USD Coin (USDC)—face complex systemic risks. These challenges span automated market maker (AMM) liquidation hazards, Maximal Extractable Value (MEV) exploitation, smart contract execution halts due to stablecoin blacklists, and cross-contract reentrancy vulnerabilities3. This report provides an exhaustive, production-grade analysis of modern Solidity practices, structural designs, adversary tactics, and the technical implementation of an isolated USDC-rewarding token system.

## **Modern Solidity Best Practices and EVM Advancements**

The execution environment of Ethereum and compatible Layer-2 ecosystems has undergone structural improvements that modify opcode economics, call-frame data availability, and state lifecycle management1. Designing contracts requires aligning high-level Solidity syntax with these underlying EVM execution primitives.

### **Transient Storage Mechanics and Caveats (EIP-1153)**

Formally introduced in the Dencun upgrade via EIP-1153, transient storage provides contracts with access to temporary state through two opcodes: TSTORE (0x5c) and TLOAD (0x5d)1. Unlike persistent storage manipulated via SSTORE and SLOAD, transient storage behaves as a memory-adjacent scratchpad whose lifecycle is strictly bound to the overarching transaction context3. When transaction execution terminates, all transient slots allocated by participating contracts are cleared by the client runtime3.

| Storage Primitive | Warm Access Gas | Cold Access Gas | State Lifecycle | Revert Behavior |
| :---- | :---- | :---- | :---- | :---- |
| SLOAD | ![][image1] | ![][image2] | Indefinite across blocks | Reverts to prior state on failure |
| SSTORE | ![][image1] | ![][image3] to ![][image4] | Indefinite across blocks | Reverts to prior state on failure |
| TLOAD | ![][image1] flat | ![][image1] flat | Transaction-scoped | Reverts to prior state on sub-call failure |
| TSTORE | ![][image1] flat | ![][image1] flat | Transaction-scoped | Reverts to prior state on sub-call failure |

The operational utility of transient storage is evident in reentrancy mitigation1. Conventional mutex architectures require writing a non-zero sentinel value into persistent storage during execution entry and resetting it upon exit10. This process incurs significant gas costs even when operating on warm slots10.

In contrast, OpenZeppelin Contracts v5 utilizes ReentrancyGuardTransient, executing both lock assignment and release for a combined gas profile of approximately ![][image5] gas1. The implementation eliminates persistent state bloat entirely while preserving traditional reentrancy guard semantics:

&nbsp;

&nbsp;

&nbsp;

Solidity

// SPDX-License-Identifier: MIT  
pragma solidity ^0.8.24;

abstract contract ReentrancyGuardTransient {  
&nbsp;&nbsp;&nbsp;&nbsp;bytes32 private constant REENTRANCY\_GUARD\_SLOT \=&nbsp;  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;0x8e94fed44239eb2314ab737b734f40c808bd702aaab5807907f187372ba69f03;

&nbsp;&nbsp;&nbsp;&nbsp;error ReentrancyGuardReentrantCall();

&nbsp;&nbsp;&nbsp;&nbsp;modifier nonReentrant() {  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;\_nonReentrantBefore();  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;\_;  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;\_nonReentrantAfter();  
&nbsp;&nbsp;&nbsp;&nbsp;}

&nbsp;&nbsp;&nbsp;&nbsp;function \_nonReentrantBefore() private {  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;assembly {  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;if tload(REENTRANCY\_GUARD\_SLOT) {  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;mstore(0x00, 0x3ee5b0e6) // Error selector for ReentrancyGuardReentrantCall()  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;revert(0x1c, 0x04)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;}  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;tstore(REENTRANCY\_GUARD\_SLOT, 1\)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;}  
&nbsp;&nbsp;&nbsp;&nbsp;}

&nbsp;&nbsp;&nbsp;&nbsp;function \_nonReentrantAfter() private {  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;assembly {  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;tstore(REENTRANCY\_GUARD\_SLOT, 0\)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;}  
&nbsp;&nbsp;&nbsp;&nbsp;}  
}

Despite these efficiency gains, transient storage introduces subtle vulnerabilities regarding dirty state management12. Because transient storage spans the full duration of a transaction across arbitrary sub-calls, failing to clear a transient slot at the exit of a call frame leaves the value accessible to subsequent internal calls within the same transaction3.

In multi-call patterns or router architectures that bundle independent operations into a single transaction payload, un-cleared transient variables can poison downstream logic12. Furthermore, while transient storage modifications do roll back during frame reversions, relying on uninitialized transient storage without explicit validation can lead to security assumptions being broken across asynchronous execution branches.

### **Custom Errors and Bytecode Efficiency**

Reverting execution using string literals—such as require(condition, "ERC20: transfer amount exceeds balance")—incurs bytecode bloat and unoptimized runtime execution overhead. In the EVM, a revert string generates an ABI-encoded call to the built-in Error(string) function, whose selector is 0x08c379a0. This encoding demands memory allocation, calculates offsets, and stores the full dynamic string literal inside memory before issuing the REVERT opcode.

The associated gas consumption scales with string length:

![][image6]

Modern Solidity development requires the global adoption of custom errors declared via the error keyword. Custom errors compile directly to a deterministic 4-byte selector derived from the error signature's Keccak-256 hash.

When invoked without parameters, the revert frame occupies only 4 bytes of memory, avoiding memory expansion and saving approximately ![][image7] to ![][image5] gas per conditional assertion. Custom errors also integrate cleanly into off-chain analysis infrastructure, allowing client interfaces and indexers to parse failure states deterministically through interface definitions.

### **Low-Level Micro-Optimizations**

Compiler optimizations have altered the necessity of historical assembly patterns, yet low-level mechanical sympathy remains critical for gas-sensitive operations:

* The introduction of default arithmetic overflow checking in Solidity 0.8.0 added validation checks around all mathematical operations. When an operation is provably safe—such as loop index updates where termination conditions are explicitly bound—the operations should be wrapped within an unchecked block (unchecked { \++i; }). This eliminates redundant JUMPDEST, ISZERO, and PANIC opcode evaluations.  
* Function arguments should be marked as calldata rather than memory whenever an array, struct, or string is read without mutation. This ensures the EVM reads the data directly from the input payload using CALLDATALOAD and CALLDATACOPY, bypassing expensive transient memory allocation via MSTORE.  
* Multiple variables that require fewer than 32 bytes of storage—such as uint128, uint64, address, and bool—should be declared contiguously. The Solidity compiler packs these fields into a single 32-byte storage slot, collapsing what would otherwise be several cold SLOAD or SSTORE operations into a single operational access.

## **Structural Architecture of Robust Smart Contract Systems**

Modern smart contract architecture isolates access privileges, partitions persistent storage to avoid collision vectors, and formalizes tokenized accounting models14.

### **Centralized Permission Orchestration with AccessManager**

Legacy access control patterns frequently suffered from architectural fragmentation. Protocols distributed Ownable contracts across multiple modules or embedded decentralized role mappings via AccessControl within disparate implementations17. This design introduced synchronization liabilities during administrative key rotations and complicated protocol timelock enforcement19.

OpenZeppelin Contracts v5 addresses these issues through the AccessManager framework15. Under this pattern, individual subsystem contracts inherit AccessManaged and link to an autonomous, central permission orchestrator15. Rather than granting administrative rights directly to external accounts, all administrative, minting, pausing, and liquidation functions reference this central manager15. The manager evaluates caller rights against a global matrix of function selectors, caller addresses, and role assignments15.

Crucially, the AccessManager implements per-function execution delays natively19. This allows sensitive governance operations—such as minting new supply or altering fee parameters—to require an immutable timelock delay directly at the authorization layer, without demanding external timelock proxy wrappers19.

### **Proxy Topologies and Upgrade Mechanics**

When protocols implement upgradeability, selecting the appropriate proxy pattern defines the contract's long-term maintenance overhead and runtime efficiency. The two standard approaches are the Transparent Upgradeable Proxy (TUP) and the Universal Upgradeable Proxy Standard (UUPS).

| Architectural Dimension | Transparent Upgradeable Proxy (TUP) | Universal Upgradeable Proxy Standard (UUPS) |
| :---- | :---- | :---- |
| **Upgrade Function Location** | Embedded within Proxy via ProxyAdmin | Embedded directly inside the Logic Implementation |
| **Runtime Dispatch Gas** | Higher; performs msg.sender \== admin check on every call | Minimal; proxies delegate unconditionally |
| **Deployment Footprint** | Expensive; requires deploying Proxy, Admin, and Logic | Lightweight; minimal ERC-1967 proxy footprint |
| **Storage Collision Risk** | Mitigated via standardized ERC-1967 storage slots | Mitigated via standardized ERC-1967 storage slots |
| **Upgrade Failure Mode** | Logic cannot inadvertently remove upgrade code | Flawed implementation can eliminate upgrade methods |

UUPS has emerged as the contemporary standard for high-throughput applications. By moving the upgrade logic from the proxy to the implementation contract, non-upgrade administrative checks are eliminated from the standard execution path, reducing execution overhead across ordinary user transactions.

### **ERC-7201 Namespaced Storage Layout**

Historically, upgradeable multi-contract systems relied on sequential variable layout or manual inheritance adjustments with reserved arrays, commonly termed storage gaps (uint256\[50\] private \_\_gap;). These gaps prevented newly introduced state variables in base contracts from corrupting the variable offsets of child contracts during upgrades. However, this approach remained error-prone, requiring manual tracking of slot alignments across large inheritance trees.

ERC-7201 standardizes the namespaced storage pattern, deriving decoupled root storage positions for isolated structs2. This approach is derived using a standardized formula that maps a namespace string to a fixed storage location14:

![][image8]

The NatSpec annotation @custom:storage-location erc7201:\<namespace\> formally registers the storage layout with static analysis tools and compiler plugins14.

&nbsp;

&nbsp;

&nbsp;

Solidity

// SPDX-License-Identifier: MIT  
pragma solidity ^0.8.24;

contract TokenRewardStorage {  
&nbsp;&nbsp;&nbsp;&nbsp;/// @custom:storage-location erc7201:protocol.storage.RewardDistribution  
&nbsp;&nbsp;&nbsp;&nbsp;struct RewardStorage {  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;uint256 cumulativeRewardPerShare;  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;uint256 totalRewardDistributed;  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;mapping(address \=\> uint256) rewardDebt;  
&nbsp;&nbsp;&nbsp;&nbsp;}

&nbsp;&nbsp;&nbsp;&nbsp;// Hash derived mathematically via ERC-7201 standard formula  
&nbsp;&nbsp;&nbsp;&nbsp;bytes32 private constant REWARD\_STORAGE\_LOCATION \=  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;0x6e26922a94f83c18b6e3f3b9c44dbdfa97b2b0ce81458e08d6d6cf5ff2ee3500;

&nbsp;&nbsp;&nbsp;&nbsp;function \_getRewardStorage() internal pure returns (RewardStorage storage $) {  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;assembly {  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;$.slot := REWARD\_STORAGE\_LOCATION  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;}  
&nbsp;&nbsp;&nbsp;&nbsp;}  
}

The mathematical rationale for the formula relies on defense-in-depth:

> 1. The inner expression, ![][image9], decrements the hash value to ensure its preimage remains unknown, preventing hash collisions with standard variable storage assignments14.  
> 2. The outer hash operation maps the result to a pseudo-random 32-byte distribution14.  
> 3. The bitwise mask, ![][image10], clears the lowest byte, zeroing out the final 8 bits14. This reserves 256 contiguous slots for struct fields without overflowing into adjacent hash boundaries, maintaining clean alignment with prospective state serialization models such as Verkle trees14.

### **ERC-4626 Vault Architecture and Inflation Attack Defenses**

The ERC-4626 standard defines a common interface for yield-bearing tokenized vaults, allowing external assets to be deposited in exchange for yield-bearing shares16. However, poorly protected implementations remain vulnerable to the classic *ERC-4626 Inflation Attack* (or empty-vault share manipulation)24.

An attacker executes the exploit against an empty vault through the following steps:

> 1. The attacker deposits a minimal base quantity of ![][image11] of underlying assets, minting ![][image11] of vault shares.  
> 2. The attacker donates a substantial quantity of the underlying token—such as ![][image12]—directly to the vault contract via a standard ERC-20 transfer without calling deposit().  
> 3. The vault computes incoming share minting using the standard formula:  
>    ![][image13]  
> 4. When a regular user deposits ![][image14], the vault attempts to calculate their newly minted shares:  
>    ![][image15]  
> 5. Due to integer division truncation in the EVM, the user receives ![][image16] shares, while their ![][image17] tokens remain held within the vault26. The attacker can then burn their initial ![][image11] share via withdraw() or redeem(), capturing both their original donation and the victim's uncredited deposit26.

To resolve this vulnerability, OpenZeppelin's standard ERC-4626 implementation enforces a virtual shares and virtual assets offset24. By artificially simulating liquidity within conversion math (![][image18] virtual shares paired with ![][image19] virtual asset), empty vault calculations cannot be skewed through direct external asset donations16:

![][image20]

This offset guarantees that share pricing scales predictably, making manipulation uneconomical for bad actors by requiring prohibitive amounts of initial capital27. Alternatively, initial deployment procedures can permanently burn an initial allocation of shares (e.g., ![][image21]) to the zero address (0x000000000000000000000000000000000000dEaD), preventing the total share supply from ever returning to zero29.

## **Threat Actor Tactics, Attack Vectors, and Defensive Engineering**

Modern decentralized finance exploits typically combine multiple protocols, capital-unrolling primitives, and subtle state deviations across atomic executions.

### **Flash Loan Capitalization and Oracle Manipulation**

Flash loans provide uncollateralized capital within a single atomic transaction, providing malicious actors with the capital necessary to distort low-liquidity automated market maker (AMM) pricing pools. Protocols that calculate token valuations, collateralization ratios, or reward distribution quantities directly from instantaneous spot reserves (such as UniswapV2Pair.getReserves()) are systematically vulnerable.

The operational flow of a spot oracle attack proceeds through distinct stages:

> 1. The attacker borrows large amounts of capital (e.g., millions of stablecoins or ETH) from a flash loan provider.  
> 2. The attacker executes a massive swap in the target AMM liquidity pair, skewing the internal balance ratio (![][image22]).  
> 3. The attacker triggers a state action on the victim contract, which queries the manipulated spot reserves to determine asset values or collateral ratios.  
> 4. The victim contract evaluates the asset at the distorted rate, allowing the attacker to borrow excess collateral, mint disproportionate reward tokens, or trigger liquidations.  
> 5. The attacker swaps their capital back in the AMM pool, repays the flash loan with a minor fee, and withdraws the extracted profit.

Mitigating this vulnerability requires eliminating reliance on instantaneous spot reserves. Protocols must implement decentralized Time-Weighted Average Price (TWAP) oracles across wide historical sample periods, or source off-chain aggregate data from decentralized oracle networks like Chainlink.

Layer-2 rollups such as Arbitrum, Base, and Optimism introduce an additional timing dependency: the Layer-2 sequencer30. If a sequencer experiences an outage or temporary connectivity failure, transactions cannot be submitted on-chain while underlying market values continue to fluctuate across off-chain exchanges32. When the sequencer resumes operation, queued transactions process sequentially32.

If a smart contract accepts oracle reports immediately upon sequencer recovery, transactions can clear against stale price states, enabling predatory liquidations before live price feeds catch up32. Contracts deployed on Layer-2 rollups must query the Chainlink Sequencer Uptime Feed, rejecting operations until a mandatory recovery grace period has elapsed30:

&nbsp;

&nbsp;

&nbsp;

Solidity

// SPDX-License-Identifier: MIT  
pragma solidity ^0.8.24;

import {AggregatorV2V3Interface} from "@chainlink/contracts/src/v0.8/shared/interfaces/AggregatorV2V3Interface.sol";

contract L2SequencerProtectedConsumer {  
&nbsp;&nbsp;&nbsp;&nbsp;AggregatorV2V3Interface internal immutable sequencerUptimeFeed;  
&nbsp;&nbsp;&nbsp;&nbsp;uint256 private constant GRACE\_PERIOD\_TIME \= 3600; // 1-hour grace window

&nbsp;&nbsp;&nbsp;&nbsp;error SequencerDown();  
&nbsp;&nbsp;&nbsp;&nbsp;error GracePeriodNotOver();

&nbsp;&nbsp;&nbsp;&nbsp;constructor(address uptimeFeedAddress) {  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;sequencerUptimeFeed \= AggregatorV2V3Interface(uptimeFeedAddress);  
&nbsp;&nbsp;&nbsp;&nbsp;}

&nbsp;&nbsp;&nbsp;&nbsp;function validateSequencerStatus() internal view {  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;,  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;int256 answer,  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;uint256 startedAt,  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;,  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;) \= sequencerUptimeFeed.latestRoundData();

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;// answer \== 0: Sequencer Up; answer \== 1: Sequencer Down  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;if (answer \== 1\) revert SequencerDown();

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;uint256 timeSinceUp \= block.timestamp \- startedAt;  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;if (timeSinceUp \< GRACE\_PERIOD\_TIME) revert GracePeriodNotOver();  
&nbsp;&nbsp;&nbsp;&nbsp;}  
}

### **Read-Only and Cross-Contract Reentrancy**

While classic reentrancy exploits violate the Checks-Effects-Interactions (CEI) pattern to drain state via re-entering a mutating function, read-only reentrancy manipulates view functions consumed by downstream third-party protocols3.

In this scenario, a core liquidity pool contract executes an asset transfer to an external recipient before updating its internal ledger of share balances or total supply3. While the pool's execution is paused inside the untrusted recipient's callback (such as a fallback receive() function), an attacker calls an external protocol3.

This external protocol queries the pool's view methods (e.g., getVirtualPrice()) to assess valuation or collateral solvency12. Because the raw asset balance has decreased while total share claims remain un-updated, the view function returns an incorrect valuation3. The third-party protocol evaluates the attacker's position based on this distorted metric, allowing under-collateralized borrowing or fraudulent liquidations3.

Defending against read-only reentrancy requires strict enforcement of two layers of protection:

* Contracts must enforce the Checks-Effects-Interactions pattern across all execution paths, completing internal balance and supply accounting mutations *prior* to releasing external asset transfers33.  
* Systems should implement transient-storage-based reentrancy flags exposed to view functions33. If a view method is invoked while an internal reentrancy lock is active on the primary contract, the view call reverts, preventing external protocols from consuming dirty intermediate state during mutations35.

### **MEV Extraction, Sandwich Attacks, and Liquidity Routing**

Protocols that perform automated asset conversions—such as swapping accrued transaction fees into stablecoins on decentralized exchanges—expose themselves to front-running and sandwich attacks if not properly guarded36.

The SafeMoon protocol's historical swapAndLiquify exploit demonstrated this systemic failure5. The contract held accumulated transaction taxes until an arbitrary balance threshold was reached5. When crossed, the contract triggered an automated swap against an AMM pool with zero slippage protection (amountOutMin \= 0\) and no transaction deadline validation5:

![][image23]

This deterministic, unconstrained swap allowed MEV searchers to drain value through systematic sandwiching:

> 1. A searcher front-runs the contract call by buying base tokens, driving the AMM pool spot price up.  
> 2. The contract's internal transaction executes, dumping its fee reserves into the skewed pool and receiving an unfavorable conversion rate due to the elevated spot price.  
> 3. The searcher back-runs the transaction by selling their original tokens back to the pool, capturing the value lost to slippage.

To prevent sandwich attacks on internal token liquidations:

* Token balance conversions must be decoupled from user transfers. Swaps should not occur within general transfer loops; instead, they should execute through keeper functions or dedicated settlement calls.  
* Protocol liquidations should prioritize intent-based settlement systems, such as CoWSwap or UniswapX, which batch trade intents and match orders via uniform clearing prices, neutralizing front-running40.  
* When on-chain AMM routing is required, contracts must compute the minimum acceptable output dynamically by reading an independent TWAP or Chainlink feed, enforcing strict slippage bounds:

![][image24]

### **Signature Replay and EIP-2612 Permit Vulnerabilities**

EIP-2612 permits allow token approvals via off-chain secp256k1 signatures, reducing user friction by combining approval and execution into a single transaction. However, careless implementations introduce signature manipulation risks:

* Caching the DOMAIN\_SEPARATOR in an immutable variable upon initialization introduces replay vectors if the network undergoes a contentious hard fork. If the chain splits, signatures signed for the original chain can be replayed on the fork. Contracts must compute the domain separator dynamically if block.chainid diverges from the deployment chain ID.  
* Unchecked return values on permit calls can result in silent failures, particularly when dealing with non-standard or alternative token variants.  
* Malicious actors can extract permit signatures from the public mempool and front-run the target transaction. When the victim's primary transaction executes, the permit call reverts because the signature nonce has already been incremented. Resilient architectures guard permit submissions within a defensive try/catch block, or check allowance(owner, spender) beforehand to confirm permissions without reverting if the signature was already mined.

## **Engineering a Secure Circular Economy Token with USDC Holder Rewards**

Distributing USDC stablecoin dividends to token holders requires careful economic modeling, gas-efficient accounting, and safe handling of non-standard token implementations4.

### **Sustainable Tokenomics and Value Accrual Mechanics**

Early dividend-bearing tokens commonly applied high transaction fees (e.g., ![][image25] to ![][image26]) to fund external token distributions. This structure typically fails over time:

* Heavy transaction taxes create friction, discouraging trading activity and integration with DeFi protocols.  
* As trading volume declines, stablecoin reward generation slows, undermining holder incentives.  
* Attempting to maintain dividend yields by liquidating protocol tokens on secondary markets creates constant downward price pressure, often accelerating sell-offs.

A sustainable circular economy avoids speculative transfer taxes, funding reward pools through protocol utility and external revenue instead:

* Value capture generated from protocol software, such as decentralized exchange fees, lending spreads, or cross-chain bridge tolls.  
* Treasury yields generated from native, low-risk real-world assets (RWAs) or short-dated government securities.  
* Dynamic protocol fees that scale down during high-volatility events to maintain liquidity, and scale up during stable regimes to fund the reward pool.

### **Pull versus Push Payment Distribution Dynamics**

Dividend distribution mechanics can be implemented using either a Push or a Pull design pattern.

Under a **Push Architecture**, the contract iterates through a list of all current token holders, attempting to transfer USDC dividends directly to each address sequentially. This pattern is fundamentally flawed for multiple reasons:

* The transaction execution cost scales linearly at ![][image27] with the number of token holders. As the holder count expands, the gas required to complete the iteration loop exceeds the network block gas limit (![][image28] gas on Ethereum), permanently freezing the distribution pipeline.  
* USDC features a centralized blacklist managed by Circle4. If any address in the iteration array is added to this blacklist, transfers to that address revert4. Under a push design, this single reversion halts the entire transaction loop, preventing all other holders from receiving dividends4.

Under a **Pull Architecture**, the contract eliminates iterations over holder addresses, relying on an ![][image29] accounting system adapted from the Synthetix/MasterChef dividend-per-share algorithm43.

When new USDC rewards are deposited into the distribution contract, an accumulated index tracks the cumulative value generated per outstanding share43:

![][image30]

where:

* ![][image31] represents the newly deposited USDC reward quantity.  
* ![][image32] is the total circulating supply of the yielding token.  
* ![][image33] is an internal scaling constant that prevents precision loss during integer division43.

When a user's balance changes—whether through transfer, mint, or burn—the contract computes and credits their pending yield before updating their reward tracking baseline:

![][image34]

![][image35]

Holders withdraw their accumulated rewards independently via an isolated pull function. Each claim executes in ![][image29] constant gas complexity. If an individual holder is blacklisted by Circle, their personal claim transaction reverts, while the broader system continues to operate normally4.

### **Safe Automated DEX Execution and Liquidation**

When a protocol converts native fees into USDC for distribution, the liquidation process must be separated from general user transfers.

Decoupling the liquidation routine preserves security:

* The base token contract should solely accrue native protocol fees, transferring accumulated tokens to an isolated treasury or distributor module.  
* Liquidation routines should be triggered independently by off-chain keepers or automated administrative functions.  
* Contracts should integrate with intent-based settlement systems, such as CoWSwap or Dutch auction mechanisms, where liquidators compete over price and execution paths off-chain, eliminating public mempool sandwich extraction40.  
* If executing directly on an AMM, the contract must query an external reference price (e.g., Chainlink) and compute a mandatory minimum output parameter (![][image36]), preventing execution if market conditions exceed acceptable slippage limits.

### **USDC Integration Realities, Decimals, and Blacklisting Mechanics**

Integrating USDC requires addressing several asset-specific behavioral properties:

&nbsp;

| Property | Value / Behavior | Integration Requirement |
| :---- | :---- | :---- |
| **Token Decimals** | 6 Decimals | Reward calculations must handle decimal normalization between 18-decimal base tokens and 6-decimal USDC rewards without precision-loss underflows. |
| **Return Semantics** | Returns bool | Implementations must use OpenZeppelin's SafeERC20 wrapper (safeTransfer, safeTransferFrom) to ensure non-reverting return variations are handled safely. |
| **Blacklist Controls** | Managed by Circle Admin | Push distributions must never be used4. Payouts must use an isolated pull pattern so blacklisted recipients cannot disrupt global operations4. |
| **Upgradability** | FiatTokenProxy | Logic and gas characteristics may change across network upgrades; implementations should avoid hardcoding gas consumption assumptions. |

### **Fee-on-Transfer Incompatibilities with Modern AMMs**

Tokens that implement dynamic fee-on-transfer (FoT) mechanics are incompatible with standard Uniswap v3 routers48.

The Uniswap v3 SwapRouter contract calculates swap quantities under the invariant that the number of tokens transferred matches the input parameter passed to the swap call48. When a fee-on-transfer token deducts a balance during transit, the volume received by the Uniswap v3 pool is lower than the amount recorded by the router48:

![][image37]

This balance mismatch violates internal balance assumptions, causing the swap transaction to revert48. While Uniswap v2 provided specialized functions to accommodate fee-on-transfer tokens (swapExactTokensForTokensSupportingFeeOnTransferTokens), Uniswap v3 explicitly omits this functionality at the router layer48.

Protocols requiring fee deduction mechanisms must track actual balance deltas across transfers to ensure internal state remains synchronized48:

&nbsp;

&nbsp;

&nbsp;

Solidity

uint256 balanceBefore \= token.balanceOf(address(this));  
token.safeTransferFrom(msg.sender, address(this), transferAmount);  
uint256 actualReceived \= token.balanceOf(address(this)) \- balanceBefore;

## **Production Implementation: Secure USDC Yield-Distributing Token**

The following production-ready contracts implement an isolated architecture. The system separates the base ERC-20 token from the reward distribution contract, ensuring that token transfers remain unaffected by reward calculation complexities or external stablecoin integration issues4.

### **The Dividend Distributor Contract**

This contract implements the scaled cumulative dividend algorithm, normalizes decimal precision, and provides a secure pull-based claim interface43.

&nbsp;

&nbsp;

&nbsp;

Solidity

// SPDX-License-Identifier: MIT  
pragma solidity ^0.8.24;

import {IERC20} from "@openzeppelin/contracts/token/ERC20/IERC20.sol";  
import {SafeERC20} from "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";  
import {ReentrancyGuardTransient} from "@openzeppelin/contracts/utils/ReentrancyGuardTransient.sol";

contract USDCDividendDistributor is ReentrancyGuardTransient {  
&nbsp;&nbsp;&nbsp;&nbsp;using SafeERC20 for IERC20;

&nbsp;&nbsp;&nbsp;&nbsp;uint256 private constant ACC\_PRECISION \= 1e36;

&nbsp;&nbsp;&nbsp;&nbsp;IERC20 public immutable baseToken;  
&nbsp;&nbsp;&nbsp;&nbsp;IERC20 public immutable usdc;

&nbsp;&nbsp;&nbsp;&nbsp;uint256 public cumulativeRewardPerShare;  
&nbsp;&nbsp;&nbsp;&nbsp;uint256 public totalRewardDistributed;

&nbsp;&nbsp;&nbsp;&nbsp;mapping(address \=\> uint256) public rewardDebt;  
&nbsp;&nbsp;&nbsp;&nbsp;mapping(address \=\> uint256) public accruedDividends;

&nbsp;&nbsp;&nbsp;&nbsp;event DividendDeposited(address indexed caller, uint256 amount, uint256 newCumulativeRewardPerShare);  
&nbsp;&nbsp;&nbsp;&nbsp;event DividendClaimed(address indexed user, uint256 amount);  
&nbsp;&nbsp;&nbsp;&nbsp;event ShareUpdated(address indexed user, uint256 newBalance);

&nbsp;&nbsp;&nbsp;&nbsp;error ZeroAddress();  
&nbsp;&nbsp;&nbsp;&nbsp;error ZeroAmount();  
&nbsp;&nbsp;&nbsp;&nbsp;error NotBaseToken();

&nbsp;&nbsp;&nbsp;&nbsp;modifier onlyBaseToken() {  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;if (msg.sender \!= address(baseToken)) revert NotBaseToken();  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;\_;  
&nbsp;&nbsp;&nbsp;&nbsp;}

&nbsp;&nbsp;&nbsp;&nbsp;constructor(address \_baseToken, address \_usdc) {  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;if (\_baseToken \== address(0) || \_usdc \== address(0)) revert ZeroAddress();  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;baseToken \= IERC20(\_baseToken);  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;usdc \= IERC20(\_usdc);  
&nbsp;&nbsp;&nbsp;&nbsp;}

&nbsp;&nbsp;&nbsp;&nbsp;/// @notice Injects fresh USDC rewards into the distribution pool  
&nbsp;&nbsp;&nbsp;&nbsp;/// @dev Requires USDC to be approved to this contract beforehand  
&nbsp;&nbsp;&nbsp;&nbsp;function depositDividends(uint256 amount) external nonReentrant {  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;if (amount \== 0\) revert ZeroAmount();

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;uint256 currentSupply \= baseToken.totalSupply();  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;if (currentSupply \== 0\) revert ZeroAmount();

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;uint256 balanceBefore \= usdc.balanceOf(address(this));  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;usdc.safeTransferFrom(msg.sender, address(this), amount);  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;uint256 actualReceived \= usdc.balanceOf(address(this)) \- balanceBefore;

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;cumulativeRewardPerShare \+= (actualReceived \* ACC\_PRECISION) / currentSupply;  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;totalRewardDistributed \+= actualReceived;

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;emit DividendDeposited(msg.sender, actualReceived, cumulativeRewardPerShare);  
&nbsp;&nbsp;&nbsp;&nbsp;}

&nbsp;&nbsp;&nbsp;&nbsp;/// @notice Synchronizes a user's reward position when their base token balance changes  
&nbsp;&nbsp;&nbsp;&nbsp;/// @dev Called strictly by the base token during mint, burn, or transfer hooks  
&nbsp;&nbsp;&nbsp;&nbsp;function setShare(address account, uint256 newBalance) external onlyBaseToken {  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;\_updateReward(account, newBalance);  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;emit ShareUpdated(account, newBalance);  
&nbsp;&nbsp;&nbsp;&nbsp;}

&nbsp;&nbsp;&nbsp;&nbsp;/// @notice Computes claimable USDC dividends for an account  
&nbsp;&nbsp;&nbsp;&nbsp;function claimableReward(address account) public view returns (uint256) {  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;uint256 userBalance \= baseToken.balanceOf(account);  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;uint256 owed \= (userBalance \* cumulativeRewardPerShare) / ACC\_PRECISION;  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;uint256 debt \= rewardDebt\[account\];

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;uint256 pending \= owed \> debt ? owed \- debt : 0;  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;return accruedDividends\[account\] \+ pending;  
&nbsp;&nbsp;&nbsp;&nbsp;}

&nbsp;&nbsp;&nbsp;&nbsp;/// @notice Pulls all available USDC dividends to the caller  
&nbsp;&nbsp;&nbsp;&nbsp;function claimDividend() external nonReentrant {  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;\_updateReward(msg.sender, baseToken.balanceOf(msg.sender));

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;uint256 payout \= accruedDividends\[msg.sender\];  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;if (payout \== 0\) revert ZeroAmount();

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;accruedDividends\[msg.sender\] \= 0;  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;// Transfers USDC to user; if blacklisted, the call reverts for them only  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;usdc.safeTransfer(msg.sender, payout);

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;emit DividendClaimed(msg.sender, payout);  
&nbsp;&nbsp;&nbsp;&nbsp;}

&nbsp;&nbsp;&nbsp;&nbsp;function \_updateReward(address account, uint256 currentBalance) private {  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;uint256 owed \= (currentBalance \* cumulativeRewardPerShare) / ACC\_PRECISION;  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;uint256 debt \= rewardDebt\[account\];

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;if (owed \> debt) {  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;accruedDividends\[account\] \+= owed \- debt;  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;}

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;rewardDebt\[account\] \= (currentBalance \* cumulativeRewardPerShare) / ACC\_PRECISION;  
&nbsp;&nbsp;&nbsp;&nbsp;}  
}

### **The Base Yield-Bearing Utility Token**

The base token inherits OpenZeppelin v5 standards and Ownable2Step for safe ownership management. Transfer operations update the distributor contract via the \_update hook without introducing reward-related failure points to normal token transfers.

&nbsp;

&nbsp;

&nbsp;

Solidity

// SPDX-License-Identifier: MIT  
pragma solidity ^0.8.24;

import {ERC20} from "@openzeppelin/contracts/token/ERC20/ERC20.sol";  
import {Ownable2Step} from "@openzeppelin/contracts/access/Ownable2Step.sol";  
import {Ownable} from "@openzeppelin/contracts/access/Ownable.sol";

interface IUSDCDividendDistributor {  
&nbsp;&nbsp;&nbsp;&nbsp;function setShare(address account, uint256 newBalance) external;  
}

contract EcosystemToken is ERC20, Ownable2Step {  
&nbsp;&nbsp;&nbsp;&nbsp;IUSDCDividendDistributor public dividendDistributor;  
&nbsp;&nbsp;&nbsp;&nbsp;bool public distributorInitialized;

&nbsp;&nbsp;&nbsp;&nbsp;error DistributorAlreadyConfigured();  
&nbsp;&nbsp;&nbsp;&nbsp;error InvalidDistributor();  
&nbsp;&nbsp;&nbsp;&nbsp;error ZeroAddress();

&nbsp;&nbsp;&nbsp;&nbsp;event DistributorUpdated(address indexed newDistributor);

&nbsp;&nbsp;&nbsp;&nbsp;constructor(  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;string memory name,  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;string memory symbol,  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;uint256 initialSupply,  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;address initialOwner  
&nbsp;&nbsp;&nbsp;&nbsp;) ERC20(name, symbol) Ownable(initialOwner) {  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;if (initialOwner \== address(0)) revert ZeroAddress();  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;\_mint(initialOwner, initialSupply);  
&nbsp;&nbsp;&nbsp;&nbsp;}

&nbsp;&nbsp;&nbsp;&nbsp;/// @notice Configures the external dividend distributor address once  
&nbsp;&nbsp;&nbsp;&nbsp;function setDistributor(address \_distributor) external onlyOwner {  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;if (distributorInitialized) revert DistributorAlreadyConfigured();  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;if (\_distributor \== address(0)) revert InvalidDistributor();

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;dividendDistributor \= IUSDCDividendDistributor(\_distributor);  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;distributorInitialized \= true;

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;emit DistributorUpdated(\_distributor);  
&nbsp;&nbsp;&nbsp;&nbsp;}

&nbsp;&nbsp;&nbsp;&nbsp;/// @dev Intercepts transfers to update reward accounting in the distributor  
&nbsp;&nbsp;&nbsp;&nbsp;function \_update(address from, address to, uint256 value) internal virtual override {  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;super.\_update(from, to, value);

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;if (distributorInitialized) {  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;if (from \!= address(0)) {  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;dividendDistributor.setShare(from, balanceOf(from));  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;}  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;if (to \!= address(0)) {  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;dividendDistributor.setShare(to, balanceOf(to));  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;}  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;}  
&nbsp;&nbsp;&nbsp;&nbsp;}  
}

## **Verification, Invariant Testing, and Security Audit Matrix**

Verifying decentralized systems requires testing beyond traditional unit tests. Stateful property-based testing and formal verification help ensure accounting logic holds under all operating conditions52.

### **State-Machine Verification via Foundry Invariant Testing**

Foundry's invariant testing framework generates randomized transaction sequences across multiple accounts, testing core protocol assumptions against unexpected state combinations53.

A dedicated **Handler contract** bounds inputs to valid execution ranges, generating randomized deposits, claims, and token transfers while tracking system variables across the test run54:

&nbsp;

&nbsp;

&nbsp;

Solidity

// SPDX-License-Identifier: MIT  
pragma solidity ^0.8.24;

import {Test} from "forge-std/Test.sol";  
import {EcosystemToken} from "../src/EcosystemToken.sol";  
import {USDCDividendDistributor} from "../src/USDCDividendDistributor.sol";  
import {ERC20Mock} from "./mocks/ERC20Mock.sol";

contract EcosystemHandler is Test {  
&nbsp;&nbsp;&nbsp;&nbsp;EcosystemToken public token;  
&nbsp;&nbsp;&nbsp;&nbsp;USDCDividendDistributor public distributor;  
&nbsp;&nbsp;&nbsp;&nbsp;ERC20Mock public usdc;

&nbsp;&nbsp;&nbsp;&nbsp;address\[\] public actors;  
&nbsp;&nbsp;&nbsp;&nbsp;address internal currentActor;

&nbsp;&nbsp;&nbsp;&nbsp;uint256 public ghostTotalDepositedRewards;  
&nbsp;&nbsp;&nbsp;&nbsp;uint256 public ghostTotalClaimedRewards;

&nbsp;&nbsp;&nbsp;&nbsp;constructor(  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;EcosystemToken \_token,  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;USDCDividendDistributor \_distributor,  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;ERC20Mock \_usdc  
&nbsp;&nbsp;&nbsp;&nbsp;) {  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;token \= \_token;  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;distributor \= \_distributor;  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;usdc \= \_usdc;

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;actors.push(address(0xA1));  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;actors.push(address(0xB2));  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;actors.push(address(0xC3));

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;for (uint256 i \= 0; i \< actors.length; i++) {  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;usdc.mint(actors\[i\], 1\_000\_000e6);  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;vm.prank(actors\[i\]);  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;usdc.approve(address(distributor), type(uint256).max);  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;}  
&nbsp;&nbsp;&nbsp;&nbsp;}

&nbsp;&nbsp;&nbsp;&nbsp;function depositRewards(uint256 actorIndexSeed, uint256 amount) external {  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;currentActor \= actors\[actorIndexSeed % actors.length\];  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;amount \= bound(amount, 1e6, 50\_000e6);

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;vm.prank(currentActor);  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;distributor.depositDividends(amount);

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;ghostTotalDepositedRewards \+= amount;  
&nbsp;&nbsp;&nbsp;&nbsp;}

&nbsp;&nbsp;&nbsp;&nbsp;function transferTokens(uint256 fromSeed, uint256 toSeed, uint256 amount) external {  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;address from \= actors\[fromSeed % actors.length\];  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;address to \= actors\[toSeed % actors.length\];  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;if (from \== to) return;

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;uint256 bal \= token.balanceOf(from);  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;if (bal \== 0\) return;  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;amount \= bound(amount, 1, bal);

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;vm.prank(from);  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;token.transfer(to, amount);  
&nbsp;&nbsp;&nbsp;&nbsp;}

&nbsp;&nbsp;&nbsp;&nbsp;function claimRewards(uint256 actorIndexSeed) external {  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;currentActor \= actors\[actorIndexSeed % actors.length\];  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;uint256 claimable \= distributor.claimableReward(currentActor);  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;if (claimable \== 0\) return;

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;vm.prank(currentActor);  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;distributor.claimDividend();

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;ghostTotalClaimedRewards \+= claimable;  
&nbsp;&nbsp;&nbsp;&nbsp;}  
}

The invariant test suite asserts that distributor solvency and token supply constraints remain intact across the randomized execution runs54:

&nbsp;

&nbsp;

&nbsp;

Solidity

contract EcosystemInvariantTest is Test {  
&nbsp;&nbsp;&nbsp;&nbsp;EcosystemToken public token;  
&nbsp;&nbsp;&nbsp;&nbsp;USDCDividendDistributor public distributor;  
&nbsp;&nbsp;&nbsp;&nbsp;ERC20Mock public usdc;  
&nbsp;&nbsp;&nbsp;&nbsp;EcosystemHandler public handler;

&nbsp;&nbsp;&nbsp;&nbsp;function setUp() public {  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;usdc \= new ERC20Mock("USD Coin", "USDC", 6);  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;token \= new EcosystemToken("Base", "BASE", 1\_000\_000e18, address(this));  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;distributor \= new USDCDividendDistributor(address(token), address(usdc));  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;token.setDistributor(address(distributor));

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;token.transfer(address(0xA1), 500\_000e18);  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;token.transfer(address(0xB2), 300\_000e18);  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;token.transfer(address(0xC3), 200\_000e18);

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;handler \= new EcosystemHandler(token, distributor, usdc);  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;targetContract(address(handler));  
&nbsp;&nbsp;&nbsp;&nbsp;}

&nbsp;&nbsp;&nbsp;&nbsp;/// @notice Invariant: Solvency \- Contract USDC balance must cover outstanding liabilities  
&nbsp;&nbsp;&nbsp;&nbsp;function invariant\_distributorSolvency() public view {  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;uint256 recordedLiability \= distributor.totalRewardDistributed() \- handler.ghostTotalClaimedRewards();  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;assertGe(usdc.balanceOf(address(distributor)), recordedLiability);  
&nbsp;&nbsp;&nbsp;&nbsp;}

&nbsp;&nbsp;&nbsp;&nbsp;/// @notice Invariant: Native supply must remain conserved  
&nbsp;&nbsp;&nbsp;&nbsp;function invariant\_tokenSupplyIntegrity() public view {  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;assertEq(token.totalSupply(), 1\_000\_000e18);  
&nbsp;&nbsp;&nbsp;&nbsp;}  
}

### **Pre-Deployment Security Audit Matrix**

Before mainnet deployment, the codebase must be evaluated against the comprehensive verification matrix below, covering known architectural and implementation failure modes.

&nbsp;

| Security Domain | Vulnerability Class | Architectural Failure Mechanism | Verification & Defensive Standard |
| :---- | :---- | :---- | :---- |
| **Transient Storage** | Intra-Transaction State Leak | Un-cleared transient storage slots persist across external sub-calls within batch operations3. | Ensure TSTORE flags reset to zero upon function exit; test dirty-state handling in multi-call environments3. |
| **Access Governance** | Admin Key Compromise & Race Conditions | Single-step ownership changes or un-timelocked sensitive functions allow administrative takeovers15. | Implement OpenZeppelin v5 AccessManager with enforced selector delays and Ownable2Step15. |
| **Upgrade Safety** | Storage Layout Corruption | Storage collisions between implementation versions overwrite critical state variables14. | Implement ERC-7201 namespaced layouts using the standard formula and validate slots via static analysis14. |
| **Tokenized Vaults** | First-Depositor Inflation Attack | Small initial deposits paired with direct donations distort share exchange rates, stealing funds24. | Use ERC-4626 implementations with virtual assets/shares offsets, or burn initial shares permanently16. |
| **Oracle Pricing** | Flash Loan Distortion | Spot-reserve pricing queries are manipulated within atomic transaction blocks30. | Use multi-period TWAP oracles or decentralized Chainlink feeds; prohibit spot reserve queries. |
| **Layer-2 Rollups** | Sequencer Outage Exploitation | Stale oracle prices clear during sequencer recovery periods before market feeds update32. | Integrate Chainlink's L2 Sequencer Uptime Feed with an enforced post-recovery grace period30. |
| **Reentrancy** | Read-Only Reentrancy | Intermediate states expose inaccurate view function readings to downstream caller protocols3. | Follow the CEI pattern strictly and apply transient reentrancy flags to state-dependent view methods33. |
| **DEX Routing** | MEV Sandwich Attacks | Automated swaps with unconstrained slippage (minAmountOut \= 0\) are sandwiched by searchers5. | Decouple swaps from transfers, route through intent batch auctions, and enforce TWAP-based slippage limits40. |
| **Yield Distribution** | Unbounded Loop Denial of Service | Push-based dividend distributions run out of gas as the holder registry expands. | Use an ![][image29] pull-payment architecture based on cumulative reward-per-share accounting43. |
| **USDC Integration** | Blacklist Cascade Freezes | A blacklisted holder address causes push-based transfers to revert globally4. | Isolate claims using a pull pattern so blacklisted addresses only affect their own withdrawals4. |
| **AMM Compatibility** | Uniswap v3 Reversion Bugs | Fee-on-transfer tokens break Uniswap v3 invariant balances during swaps48. | Avoid fee-on-transfer patterns on primary AMM trading paths; use explicit balance-delta accounting where required48. |

## **Strategic Implementation Conclusions**

Building a resilient, yield-distributing circular economy on the EVM requires aligning system design with the operational realities of smart contract infrastructure:

First, value accrual must be decoupled from standard token transfers. Attempting to execute automated DEX swaps and push-based dividend distributions directly inside ERC-20 transfer hooks introduces sandwich attack vulnerabilities, gas limit exhaustion, and compatibility failures with modern AMMs such as Uniswap v35. The safest architecture uses standard ERC-20 transfer logic, handles liquidations outside user transfer paths, and isolates dividend distributions within a dedicated contract.

Second, dividend systems must implement ![][image29] pull-based accounting using cumulative reward-per-share tracking43. This design maintains constant gas consumption regardless of how many users hold the token, while insulating the distribution system from external stablecoin risks4. If an individual user is blacklisted by Circle, only their isolated claim transaction is affected, ensuring the rest of the protocol continues operating normally4.

Third, protocols should leverage modern EVM primitives where appropriate. Using transient storage (EIP-1153) reduces reentrancy lock costs, ERC-7201 namespaced layouts prevent storage collisions in upgradeable contracts, and centralized access controllers like OpenZeppelin's AccessManager provide clear governance and timelock enforcement11.

Finally, contract security must be validated through rigorous property-based testing. Implementing Foundry invariant suites with stateful handlers helps teams verify that core invariants—such as vault solvency and supply conservation—hold true across complex transaction sequences before deploying to mainnet53.

#### **Works cited**

> 1. Smart Contract Security Best Practices (2026) \- Dwellir, [https://www.dwellir.com/blog/smart-contract-security-best-practices](https://www.dwellir.com/blog/smart-contract-security-best-practices)  
> 2. Using with Upgrades \- OpenZeppelin Docs, [https://docs.openzeppelin.com/contracts/5.x/upgradeable](https://docs.openzeppelin.com/contracts/5.x/upgradeable)  
> 3. How Reentrancy Exploits Drain Smart Contracts \- Medium, [https://arifintahu.medium.com/how-reentrancy-exploits-drain-smart-contracts-5fcd963e35a6](https://arifintahu.medium.com/how-reentrancy-exploits-drain-smart-contracts-5fcd963e35a6)  
> 4. SECURITY.md \- z0r0z/majeur \- GitHub, [https://github.com/z0r0z/majeur/blob/main/SECURITY.md](https://github.com/z0r0z/majeur/blob/main/SECURITY.md)  
> 5. Explained: The SafeMoon Hack (March 2023\) \- Halborn, [https://www.halborn.com/blog/post/explained-the-safe-moon-hack-march-2023](https://www.halborn.com/blog/post/explained-the-safe-moon-hack-march-2023)  
> 6. vechain's Profile | Binance Square, [https://www.binance.com/en/square/profile/vechainofficial](https://www.binance.com/en/square/profile/vechainofficial)  
> 7. ethereumjs-monorepo/packages/vm/CHANGELOG.md at master, [https://github.com/ethereumjs/ethereumjs-monorepo/blob/master/packages/vm/CHANGELOG.md](https://github.com/ethereumjs/ethereumjs-monorepo/blob/master/packages/vm/CHANGELOG.md)  
> 8. MTCapital's Profile | Binance Square, [https://www.binance.com/en/square/profile/mtcapital](https://www.binance.com/en/square/profile/mtcapital)  
> 9. Reentrancy | Top 10 Attack Vectors, [https://www.attackvectors.org/attack\_vectors/reentrancy.html](https://www.attackvectors.org/attack_vectors/reentrancy.html)  
> 10. ReentrancyGuard vs ReentrancyGuardTransient gas saving, [https://forum.openzeppelin.com/t/reentrancyguard-vs-reentrancyguardtransient-gas-saving/43320](https://forum.openzeppelin.com/t/reentrancyguard-vs-reentrancyguardtransient-gas-saving/43320)  
> 11. Utils | OpenZeppelin Docs, [https://docs.openzeppelin.com/contracts/5.x/api/utils](https://docs.openzeppelin.com/contracts/5.x/api/utils)  
> 12. SunWeb3Sec/DeFiVulnLabs: To learn common smart ... \- GitHub, [https://github.com/SunWeb3Sec/DeFiVulnLabs](https://github.com/SunWeb3Sec/DeFiVulnLabs)  
> 13. EIP-1153: Transient storage opcodes \- blockchain-wiki-en \- GitHub, [https://github.com/fullstack-development/blockchain-wiki-en/blob/main/EIPs/eip-1153/README.md](https://github.com/fullstack-development/blockchain-wiki-en/blob/main/EIPs/eip-1153/README.md)  
> 14. ERC-7201 Storage Namespaces Explained \- RareSkills, [https://rareskills.io/post/erc-7201](https://rareskills.io/post/erc-7201)  
> 15. Changelog | OpenZeppelin Docs, [https://docs.openzeppelin.com/contracts/5.x/changelog](https://docs.openzeppelin.com/contracts/5.x/changelog)  
> 16. ERC4626.sol \- openzeppelin-contracts \- GitHub, [https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC20/extensions/ERC4626.sol](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC20/extensions/ERC4626.sol)  
> 17. CryptoSkills — Agent Skills for All of Crypto, [https://cryptoskills.dev/](https://cryptoskills.dev/)  
> 18. Introducing OpenZeppelin Skills: Teaching AI Agents to Build, [https://www.openzeppelin.com/news/introducing-openzeppelin-skills](https://www.openzeppelin.com/news/introducing-openzeppelin-skills)  
> 19. OpenZeppelin/openzeppelin-contracts at blog.web3labs.com \- GitHub, [https://github.com/OpenZeppelin/openzeppelin-contracts?ref=blog.web3labs.com](https://github.com/OpenZeppelin/openzeppelin-contracts?ref=blog.web3labs.com)  
> 20. OpenZeppelin Contracts 5.0 Update Overview \- Rock'n'Block, [https://rocknblock.io/blog/smart-contract-development-openzeppelin-5](https://rocknblock.io/blog/smart-contract-development-openzeppelin-5)  
> 21. ApxUSD Stablecoin \- Report \- Quantstamp, [https://certificate.quantstamp.com/full/apx-usd-stablecoin/2a5be074-3d9f-49e7-aa08-46fb5f1e5bd6/index.html](https://certificate.quantstamp.com/full/apx-usd-stablecoin/2a5be074-3d9f-49e7-aa08-46fb5f1e5bd6/index.html)  
> 22. ERC-7201 base contract · Issue \#4696 · OpenZeppelin ... \- GitHub, [https://github.com/OpenZeppelin/openzeppelin-contracts/issues/4696](https://github.com/OpenZeppelin/openzeppelin-contracts/issues/4696)  
> 23. Fungible Token Vault \- OpenZeppelin Docs, [https://docs.openzeppelin.com/stellar-contracts/tokens/vault/vault](https://docs.openzeppelin.com/stellar-contracts/tokens/vault/vault)  
> 24. ERC4626 | OpenZeppelin Docs, [https://docs.openzeppelin.com/contracts-cairo/2.x/erc4626](https://docs.openzeppelin.com/contracts-cairo/2.x/erc4626)  
> 25. Build Secure ERC-4626 Vaults: Mastering Inflation Attack Prevention, [https://medium.com/@regis-graptin/build-secure-erc-4626-vaults-mastering-inflation-attack-prevention-64169912f188](https://medium.com/@regis-graptin/build-secure-erc-4626-vaults-mastering-inflation-attack-prevention-64169912f188)  
> 26. ERC4626 Inflation attack discussion \- OpenZeppelin Forum, [https://forum.openzeppelin.com/t/erc4626-inflation-attack-discussion/41643](https://forum.openzeppelin.com/t/erc4626-inflation-attack-discussion/41643)  
> 27. Virtual Shares | Blockchain Security Glossary | Zealynx, [https://www.zealynx.io/glossary/virtual-shares](https://www.zealynx.io/glossary/virtual-shares)  
> 28. Address EIP-4626 inflation attacks with virtual shares and assets, [https://ethereum-magicians.org/t/address-eip-4626-inflation-attacks-with-virtual-shares-and-assets/12677](https://ethereum-magicians.org/t/address-eip-4626-inflation-attacks-with-virtual-shares-and-assets/12677)  
> 29. ERC-4626 Explained: The Tokenized Vault Standard | Support \- Eco, [https://eco.com/support/en/articles/12068953-erc-4626-explained-the-tokenized-vault-standard](https://eco.com/support/en/articles/12068953-erc-4626-explained-the-tokenized-vault-standard)  
> 30. Consuming Data Feeds | Chainlink Documentation, [https://docs.chain.link/data-feeds/getting-started](https://docs.chain.link/data-feeds/getting-started)  
> 31. Maple Finance A-1 | Macro Audits | The 0xMacro Library, [https://0xmacro.com/library/audits/maple-1](https://0xmacro.com/library/audits/maple-1)  
> 32. Why is Your Oracle Price Feed Outdated? Here's How to, [https://www.7blocklabs.com/blog/why-your-oracle-price-feed-is-stale-diagnosis-and-fix](https://www.7blocklabs.com/blog/why-your-oracle-price-feed-is-stale-diagnosis-and-fix)  
> 33. Part 8: Defending Ethereum Smart Contracts Against Reentrancy, [https://medium.com/@ankitacode11/part-8-defending-ethereum-smart-contracts-against-reentrancy-attacks-e32915316ef6](https://medium.com/@ankitacode11/part-8-defending-ethereum-smart-contracts-against-reentrancy-attacks-e32915316ef6)  
> 34. Solodit Checklist Explained (8) Reentrancy Attack \- Cyfrin, [https://www.cyfrin.io/blog/solodit-checklist-explained-8-reentrancy-attack](https://www.cyfrin.io/blog/solodit-checklist-explained-8-reentrancy-attack)  
> 35. Read-Only Reentrancy | Blockchain Security Glossary | Zealynx, [https://www.zealynx.io/glossary/read-only-reentrancy](https://www.zealynx.io/glossary/read-only-reentrancy)  
> 36. The Stablecoin Sandwich: How MEV Exploits Target Digital Dollar, [https://www.lightspark.com/glossary/stablecoin-sandwich](https://www.lightspark.com/glossary/stablecoin-sandwich)  
> 37. What is Sandwich Attack : How It Works, Historical Examples, Risks, [https://www.kucoin.com/blog/what-is-sandwich-attack-how-it-works-historical-examples-risks-and-prevention](https://www.kucoin.com/blog/what-is-sandwich-attack-how-it-works-historical-examples-risks-and-prevention)  
> 38. SafeMoon Exploit Explained | Zellic — Research, [https://www.zellic.io/blog/safemoon-exploit-explained](https://www.zellic.io/blog/safemoon-exploit-explained)  
> 39. What Is a Sandwich Attack in Crypto? \- Webopedia, [https://www.webopedia.com/crypto/learn/sandwich-attack-crypto/](https://www.webopedia.com/crypto/learn/sandwich-attack-crypto/)  
> 40. MEV in 2026: Flashbots, SUAVE, MEV-Boost | VaaSBlock, [https://www.vaasblock.com/news/mev-flashbots-suave-ethereum-extraction-redistribution-2026/](https://www.vaasblock.com/news/mev-flashbots-suave-ethereum-extraction-redistribution-2026/)  
> 41. Panoramic Interpretation of DEX MEV: Occurrence, Development, [https://www.gate.com/learn/articles/panoramic-interpretation-of-dex-mev/1525](https://www.gate.com/learn/articles/panoramic-interpretation-of-dex-mev/1525)  
> 42. What Is Uniswap X? How It Works & Key Features | Gate Learn, [https://www.gate.com/learn/articles/what-is-uniswap-x/741](https://www.gate.com/learn/articles/what-is-uniswap-x/741)  
> 43. Multiple reward smartcontract, but it doesnt take the fees it supposed, [https://forum.openzeppelin.com/t/multiple-reward-smartcontract-but-it-doesnt-take-the-fees-it-supposed-to-be-taking/21213](https://forum.openzeppelin.com/t/multiple-reward-smartcontract-but-it-doesnt-take-the-fees-it-supposed-to-be-taking/21213)  
> 44. How To Make Cross-Chain Tokens Fungible Again: Part I | Gate Learn, [https://www.gate.com/learn/articles/how-to-make-cross-chain-tokens-fungible-again-part-i/5425](https://www.gate.com/learn/articles/how-to-make-cross-chain-tokens-fungible-again-part-i/5425)  
> 45. A technical Introduction to Blockchain. | PPTX \- Slideshare, [https://www.slideshare.net/slideshow/a-technical-introduction-to-blockchain-250927773/250927773](https://www.slideshare.net/slideshow/a-technical-introduction-to-blockchain-250927773/250927773)  
> 46. DeFi Composability and Strategy Building | AI Agent Skill, [https://www.thepromptindex.com/skill/1683-defi-composability](https://www.thepromptindex.com/skill/1683-defi-composability)  
> 47. How Mining Firms Are Leveraging MEV for Market Control | Yellow, [https://yellow.com/learn/how-mining-firms-are-leveraging-mev-for-market-control](https://yellow.com/learn/how-mining-firms-are-leveraging-mev-for-market-control)  
> 48. \`LenderCommitmentGroup\` pools will have incorrect exchange rate, [https://github.com/sherlock-audit/2024-04-teller-finance-judging/issues/122](https://github.com/sherlock-audit/2024-04-teller-finance-judging/issues/122)  
> 49. Lecture Notes on Decentralised Finance Engineering \- ResearchGate, [https://www.researchgate.net/publication/400250666\_Lecture\_Notes\_on\_Decentralised\_Finance\_Engineering](https://www.researchgate.net/publication/400250666_Lecture_Notes_on_Decentralised_Finance_Engineering)  
> 50. Beginner's Guide to Uniswap Exchange and UNI Token \- ChangeHero, [https://changehero.io/blog/uniswap-guide/](https://changehero.io/blog/uniswap-guide/)  
> 51. SBET V2 Protocol Overview & Architecture, [https://sbettoken.org/docs/protocol.html](https://sbettoken.org/docs/protocol.html)  
> 52. Fuzz and Invariant Testing: A Security Researcher's Guide to, [https://dev.to/ajtech0001/fuzz-and-invariant-testing-a-security-researchers-guide-to-uncovering-hidden-vulnerabilities-5d69](https://dev.to/ajtech0001/fuzz-and-invariant-testing-a-security-researchers-guide-to-uncovering-hidden-vulnerabilities-5d69)  
> 53. Fuzz / Invariant Tests | The New Bare Minimum For Smart Contract, [https://patrickalphac.medium.com/fuzz-invariant-tests-the-new-bare-minimum-for-smart-contract-security-87ebe150e88c](https://patrickalphac.medium.com/fuzz-invariant-tests-the-new-bare-minimum-for-smart-contract-security-87ebe150e88c)  
> 54. Invariant Testing – foundry \- Ethereum Development Framework, [https://www.getfoundry.sh/guides/invariant-testing](https://www.getfoundry.sh/guides/invariant-testing)  
> 55. The Complete Guide to Advanced Foundry Testing in 2026 \- Medium, [https://medium.com/@jaymakwanna/advanced-foundry-testing-guide-9f83a44a97fa](https://medium.com/@jaymakwanna/advanced-foundry-testing-guide-9f83a44a97fa)  
> 56. Foundry — Web3 Development skill for AI agents | SkillDB, [https://skilldb.dev/skills/web3-development-skills/foundry](https://skilldb.dev/skills/web3-development-skills/foundry)  
> 57. Introducing OpenZeppelin Contracts 5.0, [https://www.openzeppelin.com/news/introducing-openzeppelin-contracts-5.0](https://www.openzeppelin.com/news/introducing-openzeppelin-contracts-5.0)

[image1]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAZCAYAAABQDyyRAAAAjUlEQVR4Xu2OMQqAAAzE/P+nFYeKDb3jcHFpwKExHh7HsnznpBBE3R29Hwff8y7oeUtcqH6QLu1GXJQOp92Ii9zw2/MulG+4QA3Q8y6Ub7hADdDzLpRvuEAN0PMulG+4QA3Q8y6Ub7hADdDzLpRvuEAN0KXdiIvS4bR7qA+mZ6K8a27S7hPpYNoty/IPF6xhapZA1aegAAAAAElFTkSuQmCC>

[image2]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADQAAAAZCAYAAAB+Sg0DAAAAzklEQVR4Xu2P0QqEMBAD/f+fvqOHCzJtYhQRDnbAhx2TbbttTdM8yWf/3iQ9L8394EM4p1Qv6fM/54Ke85JVKLmUw3XVbro0N+GKK5/gemovXZqbcMWVT3A9tZeec6G85VbpgOuq3fScC+UtlwvA9dWF6DkXyksuhQVuh7oQPedC+SVx8AS3R12InnOh/EQcDHB71Dn0nAvlT7lV2nFddSG6NLekyvyOrJzC5dQeujQ3wUeoBw2UH7Dr9gzKu8wgzd3myaXprjTXNE3T/A9fliaVaw6w63cAAAAASUVORK5CYII=>

[image3]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADQAAAAZCAYAAAB+Sg0DAAAAzklEQVR4Xu2PSwpEIQwE3/0vPYPDNEiZ1ihuHqTARZcdP89TFMVNPv91g+w5t3s/+BHmHTjHLOiZBT1zSFQ6+ZSbobvdG5gNRt7h+nS3ewOzwcg7XJ+eWdAzC+ennAy5GXpmQc8snJ+yPfD4i+iZBT2zcN6yVQbRg/gAZkHPLJwPSRcn8BN8ALOgZxbOD6SLm/BMdw89s3B+ye5QdFHWNeiyvRANc/VErifaZ25EvQZdtjfAT/SLOC9W8z3aX3WzvWNWh+5cfLtXFEVRvIcvj0atUzZy2DUAAAAASUVORK5CYII=>

[image4]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAD8AAAAZCAYAAACGqvb0AAAA7ElEQVR4Xu2PUWrFMBDE3v0v3RLoFKOsbIdnWmhX4I+RZzfO69U0zX/m4+vssNtbsfvN071vOMA8Qs+8C7/BHOiZAz2zUpWq4cpdVG7Gkz2n3Y3ZY0bPHCo348me0+7G7DG7P195w/r0zIGeOZhfUg1W7sK8YX165kDPHMwvqYZsmXnD+vTMgZ45mJ9iA7bMvGF9euZAzxzMK7OyLTNvWJ+eOdAzB/Mlq7LdmzesT88c6JmD+S04aMsqN+PJntOuJA/iGancBZ31gt3/hLvBHx5PRfyqY3dhvJ91T/feZmf5buc3ek3TNE3z1/kEpt7XKd0TEYIAAAAASUVORK5CYII=>

[image5]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAZCAYAAABQDyyRAAAAmklEQVR4Xu2OQQoEIQwE5/+f3kHYFq1NZ4IM7CUFHrpsY66raXY+31Ph1R4/Zl6hZxb0zBvRZbRE5AZ01d4ke7B6ZkFX7U2yB9UFTnopUTlyA3pm4XxIVHQD6JmF8z+4khtAzyyc38gKbgA9s3B+8lRw9/TMwnkLy24AXbW3oUc8K5Eb0FV7E37qFhDyWWdQ7R1RHVjtNU3zH24MM3uFvOM9SAAAAABJRU5ErkJggg==>

[image6]: <data:image/png;base64,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>

[image7]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABUAAAAZCAYAAADe1WXtAAAAeUlEQVR4Xu2PSwoAMQhDe/9Lz6CMYNOkH8rsfODCl1Roa8VfPCg+lDcsm+VOlPIwMMO9Y3UsYDlzjgwA1mPOkUFC/UT5LlClUz9I3A31WHkKFtVj5SlYxj2gnso2etwD6plkzth1VF4fNeJIHkXOZj1ndSxz0i2KG14luFCwZBuhcQAAAABJRU5ErkJggg==>

[image8]: <data:image/png;base64,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>

[image9]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAPEAAAAZCAYAAADg3MjmAAACt0lEQVR4Xu2VUW7jMAxEe/9Ld8EPAtzBjEivrUTJzgOMho8jiXJa9OfHGGOMMcYYY4z5i18U305c+JMufXXeLq96yifdvkHXN3uYfDdfx6ddeDIvfpFYV7JXHwX2sE6UN6/hhPc//Z16hO0HPMxkXpZRL3P6orG/WqO8eR0nfQfbZ9l+wMNM5lV/YMxjzWDrzNmc9H1tn+XqAV3+Tn/yx9L1A7UP81gz2DrFNDfhyrl3Oe2c7u6rXtCtfyXb58AD2OXRYZ2ufr7S7+oK+lW2onLVdxmckaF8wPZgefRYV9RsyiHoa83yCTujegQ91gn6q3Wi/DvYPse/vpDVurt1Oka3TqFy6LEO1DlTl7B9sA6muUBl0WOdoKs57CGsvzrn7jxZV7CfKP8Ots+RB6wOYi+kOtavdH2Gyk/mRa5kA8yr+ZnHusJ6zDFUjnk111WXn1kuYC5QvsL2ZK7C+swFyiN4R/Xc4e76lsmwmMEs1kjXT9T+lUmmMskguDfWCfNYV1iPuWRyV+ZZfuXYozIVrBOWDXAvzDBXwbVqn0D5Cu6xeu5wd31LHVId1l1kRx/rZDJvwvatqD56rBPmsa6wnnLosU6YV+snjpE5zKu1mGMOa+UqXb9yJbub7XN0LzZY+fz5dB/rZDKvArNs/dQFU5ewnnLosU6YV+snrsJ61ak++s7Vn5irdP3Klexuts+BB7DLM1fZ0cc6Qc/WBunxqWAdqBy6YOoS1lMOPdYJ82o9umDlVj38nLBzOod7siz7nCjH/DvYOkdeVD3Irn7nsVbPJIdgn2WSSY55tg5dXdd5rFePylVUDz1blz9VJmEZlWfZStcPlH8VOGM3r7nJlZc7yU0y38DJ9zx5NvMB/C+/QKfe89S5zAdx5T/7J3PqHU+dyxgzwH/A5lH8C2WMMcYYY4wx5/EHn9KPjaH2MKgAAAAASUVORK5CYII=>

[image10]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAALMAAAAaCAYAAAD8B23VAAACUElEQVR4Xu2T4Y7DMAiD7/1f+k78QEKWATdLunXHJ1UTtkNI2v38DMMwDMMwDEPLLwofzi3z2ia3bDRs493vS9lfyWzjiR/x02b2ebu51ZxR+e4pfVZQ54xzRLp1yxxrfJgTM9/VU9G695J5qGO9g/iRZv2rDNO2cKzxYU7MfKon9kXN6y7nrOg7Ufp1mc5fIl7AkQ0OsXvW7EN4FdYXNa+7nMM042p+FaVfl+n8JbqLZN4n4DN1czIfNfYglc96Z3R+JMsyzajyla7MHrO4zkGPZSKVt0S1YeW9GzYb1g7TcT3WEfRijZ5rDJatyPJMM6o86lfOE6k8p+vhKJlL+MasMdNWyC7uFbIeTFf2zDKV7r/Mz1DzVSbzst6oYyb66CGdb+B+GUpGJh6ANWbaVVhvrFfIelzVHTan0en4KHRZxWdk6zLdqbxI18e5ktsCbsjqHVR9cL8qi2TZrE/UOz+S6Yjn4pNR+ZkeyTJZ30w3Kg9Rs0rGUHMtbDCsd9D19Dm6HJLlK909lslmyHQHvXie7GxMM5iOtcE0g603mOZkaxhqVskYaq4lGyzTPw02Yzd75Xce4hpb5xrzjE7HB2GaoeZjjnkZWX9EyRhqriUbjOlYfwI4J9aMKlN5Bnpes3VRQ8+o1rAHYZqDHtZGnC36WCOdbygZR83JVJtn+nCd6p6vovTq/BWUnkrGUHNDwrdcoPIxn0DZU8kYam4I+KV92+XddR7l/vzPpf7J1NwAKC/jqdxxJuX+lExEzQ3/jKd9GE+bdxiGYRiGYRgezR+aRcVJa/31nwAAAABJRU5ErkJggg==>

[image11]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAC4AAAAZCAYAAABOxhwiAAAAmklEQVR4Xu3SQQqAMAxEUe9/acVFSvmk6UTEFsmDLhKnTRYeRyllpZMNugP92UVqHzn4gdQuqfBOViz+yswnj/BfZG09Ym5Wh+RghwNYW4/Y4z3WITnY4QDW1mM967EOyUHwBlrPe7PP8DAjkYPgDVEWjyiZRg46eDcaHH0zSqaRgw4OYk3et8z9FvBOhneHNY3mjfqllFJ+4ALhLmmXqbG5swAAAABJRU5ErkJggg==>

[image12]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAALYAAAAZCAYAAACcutQ/AAACLElEQVR4Xu2SC2okQQxD+/6XTiiCSfGQXE6P05mAHywbyfKni7muYRiGP+SDxvXlKX8Y3p748WY/4Kw2DG+L+mGf9HCTroeszunOPUH1llPO/bB3j/Xh+n4kPpaCdeoq7KMO6FMH9Kmf4jfe0s2q7hmu/JHcIyovozqnO/c02X5Vy75D+cGpPlz5A7kHVF5GdU53zlHJVTIk61G17Dvon/S78md3ZovVAy+c73B5+tQBferA+Yosl9UyXJ+76yf+SWeoeYrIqGxWWyi/svc09zbZQHeY8x0uT586oE8dON+hssqr4nrdXcoP71SrwCx1QC+0ymfzqMMj1dxLZAPVAQvnO1yePnVAnzpwfgbnvoLrd3c5vws1n3pBL/Sp/1RXelHpe5lsoDpg4XyHy9OnDuhTB84/cbePuBluvvN/E7Uv7uA9zg+UT4/1xWluC9lgt9j5DpenTx3Qpw6cf+JuH3Ez3HzndxN73D7W9wz9U43zqQP2uNxtsoFuofMdLk+fOqBPHTj/Kdxud5fzu1DzqXciz76Tn5HV3dwWsoFuofIyqnO6cydUXnlVsl5Vc9/RhZpPrYg+ld29aoZ/n3payAZWDg9Nb8fV6XXnnibbr2ruO7pQ86kX9KLv1K/qhPn4n33Ut+Dh7iOC7KAgqwWVOYvuHKlkK5lF7Fb/yO6rejfuHurdUzeq2k61vuvdZ/1RKou7Movu3DvxH28ehmEYhmEYhmEYhmEYhmF4gk9atd8vhmZHUwAAAABJRU5ErkJggg==>

[image13]: <data:image/png;base64,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>

[image14]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAKwAAAAZCAYAAACsNsUeAAACEUlEQVR4Xu2SgU7DMAxE9/8/DYrAUvR057jFFBB+0rTd+ey4WV+vYRiGC7zReH14yh+GHyNeyuzFzGrD8DjqhT3p4eUvxfkVqr3duSeo7nLKuRd291gfPomL2j93YB91QJ86oE/9FFfuhnXqwM2qnvOv6bgk10+vO/c02fmqlj2H8oNT/V/TcTHugul15xyVXCVDsh5Vy56D/kn/Vh7fs+NA9Qcs6FMH9KkD5yuyXFbLcH1uryv+SWeoeYrIqGxWWyi/cu5p7mX2QysLKFwffeqAPnXgfIfKKq+K63V7KT+8U60Cs9QBvdAqn82jDo9Uc7fgIOoKasEFfeqAPnXg/AzO/Qqu3+3l/C7UfOoFvdCn/lNd6UWlr5Wrw9WCC/rUAX3qwPkn7vYRN8PNd/53os6LPbiP8wPl02N9cZrbztWDXJ4+dUCfOnD+ibt9xM1w853fTZzjzmN9z9A/1TifOmCPy13CDXK+w+XpUwf0qQPnP4U72+3l/C7UfOqdyLPv5GdkdTf3NmqQ8k64HnrduRMqr7wqWa+quefoQs2nVkSfyu5eNcPfp57bqCFqSeXtuDq97tzTZOermnuOLtR86gW96Dv1qzphPr7ZR30bLu8GZ7UgW3inO0cq2Upmsd8LP2T3Vb0btw/17qkdVW2nWt/17rP+ZaoDuzKL7txv4i/uPAzDMAzDMAzDMAzDMAxDL+9GhcZITcSz0AAAAABJRU5ErkJggg==>

[image15]: <data:image/png;base64,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>

[image16]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAsAAAAZCAYAAADnstS2AAAANElEQVR4XmNgGPrgPxLGC9AV4NSETQKbGBjgksAmNqoYBVCsGJsYCoBJElQIA0QrHAVEAwApICrW6VSvhQAAAABJRU5ErkJggg==>

[image17]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAHIAAAAZCAYAAADt7nrkAAABdklEQVR4Xu2R0WrEMAwE7/9/uiW0AjPsSnbOZ3KggTxotLKc5PVqmmYLPxSvP6d880DiZ2U/LOs1D0L9yKpOcWHnZ5id3Z07wexdqpz7kaNjvyQOGJ87cI51QM86oGd9ipVvwz7rwJ01u0fy1vA/bp5ud+402X7Vy95D+aDqS5YHBG4x3e6cYyY3kyHZjOpl70Ff1SXLAwJ1sQt61gE968B5RZbLehluzt1rxVd1yXioWjCDm6NnHdCzDpx3qKxys7hZdy/lw1W9ZTjEega3nJ51QM86cD6D576Dm3f3cv4Yq8vdhelZB/SsA+cr7s4Rd4Y73/ljrF7A5elZB/SsA+cr7s4Rd4Y73/ntuEXOO1yennVAzzpw/hRut7uX89tRi5SrcDN0u3MVKq/cLNms6rn32I5aopYrN+L6dLtzp8n2q557j48Qy8ZHkfWC6FfZ3Tkyk53JXIzfhQ8Zvep/HHcxsitzsTv3JL7xzk3TNE3TNE3TNBm/EIMk6icPNCQAAAAASUVORK5CYII=>

[image18]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAHQAAAAZCAYAAADg8AqjAAABSElEQVR4Xu2Ri2rEMAwE7/9/usVwAjFoFTt1D+fYAYN39bASvV7GLPLzPicRM83OlfNVDePUX8VfPuo/f8pM3yqHHhfOs8qdmo9y6oBXc6mF0GcO9SNYGbrKrbyB8u/S9WMsFhU+48HqQrue1FvIH3L1AOPUA3rq49WHco47/UJX92Alnqne6XTAnHyv8rfQNVYP0+s076FZk2GMPfKduUHls5ZU3oDvzGjCeJWzha6xerjyMhy+QvkDxlQ/zqfugfLCZ7+A/pUO2PsjdA/NDBo6MxOjn2FM9eMcmSrGWt6rmgH9K53JvTPU2+gaq0Hph+ap4hn6rO8O85WmX3mkyq9ilVbejL+FrpF6SPnmALrFqMUp3xxAtxi1OOWbA+gWoxanfHMA3WLU4irPHEK3HC/0IcSiqlMRfpdjHoYXaYwxxhhjjDFmlV+A5RP72jUQfwAAAABJRU5ErkJggg==>

[image19]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAsAAAAZCAYAAADnstS2AAAAJElEQVR4XmNgGD7gP7oAMgBJomOiwKhiZDBUFMMUYMOjgM4AAF5vIOBAZRbZAAAAAElFTkSuQmCC>

[image20]: <data:image/png;base64,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>

[image21]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAFcAAAAZCAYAAABEmrJwAAABI0lEQVR4Xu2Q224DMQgF+f+fbuWHI7lT8IUllZIy0ip7BrDJmjVN0zSfwBdFwE3fae+rudpDi1f8Ac4zC3pmQV+x4xMe3Z8etPhiuuq+vyZ9f3rQzj9Gdd/b8GTx1ceYPbOgZxaRr6b8jicHRn+anlnQM4vIE6/Py6s7meVSpAfNX2RAzyzomUXkPdjH2V1dbpWPSQ+av9iAnlnQM4vIe7DXyzOse471Y9KD9nsJQc8s6JlF5D3Yy0xU5zPDfEx60PxFBvTMgp5ZRN5j7uWvx8nZu3pIetDixeiq+3bwo+pc75yV996vWA1GF4uoTlfdt8M7x3ODyM/s6j/Qgd5DIj+j+q73to/vN3COmUTfIfJlnBx60jO46TvtbZqmaZqmaf4335E26ReHIW7qAAAAAElFTkSuQmCC>

[image22]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAE0AAAAaCAYAAADygtH/AAAAvUlEQVR4Xu3SjQrDIAxGUd//pTcYC7hLokatXeE7UFjE/DRrKSIiIlJe30cStLQJWtiEpaXZZ2pFdn+2rM/zO7B3NKPLS+TvXVjvih6jot7e2Q9e4NJ6osa11p/A+CSbp55hap5sEpu2ePe8s1Mys4dmiozmePe8s5Os99IcS8kdXm3GEcsdfUbw7mjeR53MRMYrvCF31s9ib8ZN9cKufCnWY3waezP+S3cv7RG4IC2tgwvSspK4QBERked4AxVeco4z+9E9AAAAAElFTkSuQmCC>

[image23]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAmwAAAAxCAYAAABnGvUlAAAEj0lEQVR4Xu3U627bSAwG0L7/S3ehH9MlviVnZCfexsk5gGHehpJcNb9+AQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAP/6nYUf7Cv/Fl/53jrvdr/wjvw/439TX7YrfsXLl9fIWufUf1Q+26P782z3HLXWxSuvuj1/00fuY/ecJ6ffqdPN557P8si/03RfO6f+d3b3N/qIV+6+vGp/7j3ly1Rfnul3tZ1r/pkz7+hd75s3ky9a5p/t1fsnz/zxqPJs5pdauxN/N/lsme/kbOYnr/6Nn91599zdubs+e9+7yefP/FnTnqn+Ubn3lN91Onfq3/EZOz7Lq+/l1ft5I9fLsF6IFXe17C/ZqzJf8jq5I8/dmbl0tctufre75vX8Ls/rTLNZq9+dqdftqXlXW9/d2bv1rrby7rP63Vw19XLHkvXpO2U/r1d19bzH7nydqb08k3t239VUO12v1rOXM7VX86o7l3trrcqz3Y4a52xet8p65kvurHJ/d82uNunmpvNZW/FprqtlnqZ+1u/MnOR8nl39nMm8q9daN7/inMn5JevTubszWatqD/6jezHypdnNdGrvNDf17+5I3exu19Trnr2rLfVZujO7uOZZr6bebu+l3tsjujPTtaZ4pztT7zX3dPUuns6lqd7pZrvapbunjFM3t5tfcmbK83uKT7Wlm6vx9d3VT/F0bqpnnLKXedXt3M1Xd+e7/nTd3NnN1fhubZL97my9r6W71l3d2S7udnf3UuWenM1+1mp+Z3bpZqe43lfe47SfH269KKcX8fLITMad7Hf7c2anm5121WdeeZr662y930fPV5l3ppnd3mrX60zz9ZmzlvHOdKbb3+WXO7XML11tp5vPWnffU7zy05mTnJ3yda3Tdab+7my35/LsTN7z0sU5k7KXeTXtr98Zp7u9KV6mfs5mXl29PHuan/IpXk67q25XV6vxtHuqX7I35d31Mq7Ws3bnaz7Vq6zduT4/WPeCdLXMs17dOb/i9el6p7jT9Xfnp+sv3dmpdvd8xnfyS1e77PZWu16nm5+uNcXLqdb1Uzdzqq045zI/6ea769yNl+7+priT/SnP74yXrv/sXK1PM1XO5GyXZ+0jputeds/b9TqnualfnzPPZZ6mc52cybP1O2cvXa3TPdujO7OeeefONaZ46fr5vWS+dDu6PHvw5yXOl2P3Et7p1Tw/U6/WV7xMuzPP+pL1nK/XnPLu082krOdsnt/N5/6sTfnu3K5XdfWsddfLePp0M7va0vUyr7VdPftTvfYyr/Ws7erdroyX6Vz2ulpXr/Hus9S45lm/5LldXmtdb6nXy5kpn+o17mbyXvKaGU+7Lt2OjJddrcr76Worz7kq7yPPd/HKu9opn3Z295q17HWyPp2Z4pVnf6plXuvZr/HpmqsG8KXkH6bM4eSZd+aZM9/Bq577VXu/s91vtusB/FX+QH19/o3g9fw/AwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAgJ/iH2BOymBWpBtPAAAAAElFTkSuQmCC>

[image24]: <data:image/png;base64,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>

[image25]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACcAAAAZCAYAAACy0zfoAAAAsUlEQVR4Xu2QUQ7DMAhDe/9Ld6pUJurZhqT75EmRio0J6XEMwxLnfeJb4bxtqqHoY33BtB/ilfm1CvSxDpSe6fQ8cAG1fFfLVD7Fhf653BZuqFsOdawzzrO4IFviotKzx/rauDBeFCi9w1LONasllJ7BHqxbuIAaqPQM+li3cCG1hNIz6Fc1xTWpJZiWYT5qWFNc085yykMd6y9xKTuM0F1PxZtsSWdw1VP9hGEYhrd8ADfDZ5kuZnNsAAAAAElFTkSuQmCC>

[image26]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACcAAAAZCAYAAACy0zfoAAAArklEQVR4Xu2RUQrAMAhDe/9LbwzmsFk0Sn99UJgmae261jC0uN5l3xGZ1iLaiPWxh/UD6/2wW/rbRqA38kd9T8WzoQJqKONUp6iQ0o2qr4XaVOlG5su0FBX0T6qe13TvyfwSFUYd6y6tfMv8UsmwP1jJbbQDq3YQ6liXyELREFHfg7qqKZmJDcF6CNOxhzUlMzFNDRdp2Mf6ww5gC0GdeSqcZFOqGyvP6QWHYRgUNzaSY50fg3SbAAAAAElFTkSuQmCC>

[image27]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADQAAAAaCAYAAAD43n+tAAAA3ElEQVR4Xu2SQQ7DMAgE/f9Pt0oVIrJhzeLIPlQeqQfDLASprW02m1V8zl+G4lR5PdMG4BH2ZgtY3TM6g9VTogM8Ua3C0oPwGEb0QfiO8Mcwn9UPer0HuKQXRtdqGTgfM1HN0+vdyAYh6OObkWXwjUSZEFk8QVfNo4M57CPoU2SxxW5UU6jmZF8WW+xV8p5qTvZVkXms7mF9y7K+R/VkkTlKnvWnHHTQG8zqxuy+oXo//EE+hO+IzHnbN1TvwUiw6o+wYsfFimUrdtyYuXDmbMrIX1Vh1tzNZvPvfAFU25hoVNowsQAAAABJRU5ErkJggg==>

[image28]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACgAAAAZCAYAAABD2GxlAAAAuElEQVR4Xu3OMQ7DMAxD0dz/0i0ElIEqfzpKu2TQAzyYogwfxxjP8vqcjl1P73Tfu+zToN6l5vWe0bvV9mNChW4WKJPOzL17okI3C5SJ2wntDxJaoiy4XHazcLW/cAt3c6F5vtMcqejKbuZyoflPH8xoibLg8qx+KOvsL2iJsuDyLHdqt7O/0FJerHdxefbXB6lw94Mdu33KT1ToZoEystun/ItK+TiauZ57x93rsS4LSbc3xhhP9gakiJpm7HNC2gAAAABJRU5ErkJggg==>

[image29]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACwAAAAZCAYAAABKM8wfAAAAzklEQVR4Xu2QQQ6EMAwD+f+nWRltpMVKYgNV90BH4tBkUqds22Jxm/37KRxnOLxcnLnOOP0O1U/JFv0lq3W4jwWOc4IHsuEqnM8Zo5wDXqIbZDdqilHOAS/bDXKfzxWOA6TnBgbsuvOOA6TnBgbsuvOOA6TnBoLMc+cdB0jPDQSZ5847DpDelcDMq+qM4wDpRWAnql7XDxwHWF63dFUPVD9wHOB6p6W7BzCdx3epe6t6S3dhxVW/YtQ9U7jzox7xNGz6wmB64L94zUMXQ/kAvPeBfzs9BIsAAAAASUVORK5CYII=>

[image30]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAkUAAABrCAYAAAB5R/auAAAD6UlEQVR4Xu3ZUa6kOAwF0Lf/Vc0OZkkz80aNFFl2EqAKQtU5EhLYCbi6P3LV/fMDAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAwLf7589VGfUBAB4thp0YfNp+7AEAfIyZUAQAfKgYBGZse6rrLrPfnlmXrVnldwIAb3DmkM/2ZbWrjL7bztZbW/2Gtpb1AYCHagPCkUO+2nP0fWf1vpn1RnPG3ugZAHioM6Got6fXe6feN7NenHPmuRWfAYAHigd6DAAjvfW93qwj+6s91Tyxnj23ej0A4KHiob4FglivVOte9Y4jqn3VTFm99+fQ9rI+APAw1YE+e9jHcDC7b8aZ91R7q/mqOgDwJaogMBsSqnVZbca27+j+TbW/N29WBwC+wCgEzASFak1Vn3F0X6t6RzVXVQcAvsAoBMwEhWpNVR/Z9hzZ26r2V3NVdQDgw80GgFFYqHqjfZm963t678p6R+YFAD7AFgJmr8zRXqZaW9VHevuy3t55AeCQ7MCJzyuJ86486xHb79t7bWK97W1G/daoPyt+s/f9tp71AeDl4uHTO6juls263bPfqn/PrdXnA+BDVAdOVb9TNVNVBwCYVgWKqn6naqaqfpfV5gEABnqHd693h95/81T1u6w2DwAw0Asaq3narADAw2xho71WFedcddZV5wIAOmLIOBs24ntG115x/5F3vNuKMwEAO60aNDIrzBoD2uga+eu/62/XWy8AmFId3lltBdW8R+19Xww9owsAeIjq8M5qmRgCRteM3rqsl9X2uHs/AHCR3qG9J6xcYTRP1stqe9y9HwC4SBU0stqvqn6F3qx76nvcvR8AuMh2aG8Bor0yVf0KR2aterPu3g8ALOgVIeNKr5j17DvO7n+HGCh7FwCQaA/KJxyYr5j1zN4VZWFntgYA/PG0f0E4O2v7e8+8ZyXZ76h+X1YDAPhYQhEA8PWqQPSrqgMAfJxeKAIA+BpCEQDAz/2h6O7vAwD8b4VQcvf3AYAvt0Ig+rXCDADAFxuFolH/Va74BgBAqRd62nq8j8/V/eg5u4/PsQcA8FIxpERVP9ar+/ic9bZa1svuAQBuk4Wg+Jzdx+esV4WiX1kNAOByVSi5MhRldQCAS22hJAsnsdeGm1jbxDVtPdbaOgDA4/RCTK+X2bseAGAZvSDT67Vm1wEALKn6b7BfvV40uw4AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAPsm/pqd21uSQuOEAAAAASUVORK5CYII=>

[image31]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACEAAAAbCAYAAADyBeakAAAAkElEQVR4Xu2PWwqAMAwEc/9LK0gibc3mJViEDOQnOxsrUdPkOHi2UnmEdNCkKBcZ1EV7lVd/QLgTvjdKlYdYvpVNrFK4yFi+ld1oQqjIIBftVTRRDmjZyuhmejeWHD2GPLR/4EmRQ8hB+zSRQ8hB+wlXoNghlLtdETKjUc0u1g9ER1j3YyZ4+Wdsf0DTNP/kBIKsfYOSw89GAAAAAElFTkSuQmCC>

[image32]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADcAAAAaCAYAAAAT6cSuAAAAsUlEQVR4Xu2SjQqAMAiE9/4vXQwS5DhnC6Vt+EHkncsfVmtFURTBXM/zxVseNjTzOszbjuOXY1j+Nli3dgS1XCLSP2WGtMITpMyQUvQDKXN4Rb18FCl9RkW1jzFqFnsa45Gexitg5dG3YtHoaSSH51CngY2YZrFo9DTWcuLpdyhWURzEikWjpxkt12FeCNKQNcYcDsm+ETCPWsO831hqmGgiltM3ugze7zXKI2/OFMXq3McUfIR1rBbwAAAAAElFTkSuQmCC>

[image33]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACUAAAAZCAYAAAC2JufVAAAAmUlEQVR4Xu2OUQqAMAxDvf+l9ceCPJo4pZuieyDYrE2yLD9j3T/F2XtXsnDOQzgWYamuhVrNb5eKQxpk8J1zoLxuF1S0BBHeuF2JO2JAQI0lOB/hnOKWGBBQ5z/ny7gjBgSZHprT+SZxi8pI6WU4cxWu9DKcuQpXehnOXIUrvQxnrsIzrRQXMLRUhGVfRuhu5xFeVWYymXyWDfqhZZt0Yqs3AAAAAElFTkSuQmCC>

[image34]: <data:image/png;base64,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>

[image35]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAkUAAABPCAYAAADlerGOAAADCElEQVR4Xu3W0W7bMAwF0P3/T28wMAHCHSlbTdvY3TmAkPCKZuW+KL9+AQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADcxu+/KzMAuKVxcXXrp9h9r+zP9VGfMeMJ5nf8rP8dAHyL7sLq8qfafZ+uv8uv2nl2p/cOuvN2OQDcyuqSX+09ze67rHp3Z812ntvpvYPuvF0OALeyuuBXe0+z+y5nvbvzhp1ndnrfbXXW1R4A3Mbqcl/tfaWv+Ju773LWuztvuPrMR+e/y9POCwD/6C6zLj/k3lk9sqzPsqyHkc9rlvWh6ls5663mZZb1Tnaosjsb7zEvAHiMvMSuXGbVfmZVPWe5f8iekVW6WdWMQ5d3znqreVkfMsv6UM06VNkrxt+5unbl8x+dAwBv0V1cr+ZX6iu6vlVe7XV556w352U9ZF71HKq8yp4k3x0Abq27uM7yas0yy7qTM7tnVnm11+Wds96cl2fuzp/1sNP7FNU7AcBtdRfXbl4Zfd3nrJtbZYdVXu11eeesN+dl3el6qjznv2qc8ep61WfN+Up3Px8A36i7uHbzQ+ajnj+751f5/DlkPazmVHln1VvNqrJhzq/0DFeee7fVubr/SZd/ht25u/0A/GDdBZV59pzVQ+Y5d6jyOav2Ork35mTe6fq7fJZ7VT1nq5nZN1vtfacrZx+yd/U96/mzynIv6+p7VQPwHxoXR67ZnHV71XOz3Mt6Vs3M+dnTzcv9rDs5O9eZq/1X+qr98b3K3mE+T67U5Yd8n65vyP3V8933qgYAHiQv/adYnTt/uHR9Q+5nPcvZs6wBgAepLvIqu5vVj5384dL1Dbm/qrvvc505APAA40fDfKE/5VLPs8/mvWpVfbPM8/nczx4AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAeKc/FUIBHMhUhzsAAAAASUVORK5CYII=>

[image36]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAALsAAAAaCAYAAADv0C0hAAACHUlEQVR4Xu2SgWokMQxD+/8/fYcLBiMkx8lk7pZWD5ZdS4qcmfbryxhjjDHGGGPMm/wpH/OPefPFv9n9SayeUb0HpZ9wq+eU+iz/+y6Smy8cebP7U1g941N/yo2OJ+B+nH8Ft/6Yn0r3fJ2XTDITph239lVY3xt7PpZ80J/+0Or5lI5Mcx0nHbv5DtZ1cidKFmVZnesCpiU7nupXsDsg2IczaqwjwZzqQFDDrOpknvJXsJzqDKqG+1l+xem5RJ1X+jZZwsrYg+OcWv2uTLyOyW78VFDDGUGv5vE7YZ0qG7B8wLRA5RGWU/dg2YBpu6juFeqc0o9hZUqren2ZLJ8wj2kV9NmO1X7Uulynd3twrjBvpwP3d2Bu984s94TdPpVX+jFYphbs6gl6kzz6TEuYN9WCqY5zagrm7XSwrEJlmY5zwHI3mPaqnNKPYGVMC5gWqHzAPKZVlNfp6OEcsFww1VdzRXmoqVzQeZUuhx7OidJP2e1TeaUfwYrYAqYlSg+Y13V1qHM72hMdM+hXpnrXEdzwcUYtYNopascKdua0i8KK2AKck6qzzErD3yyfKB+1VQ49nIOJVvcwD6laPceySed3XoK+urP6PWVylxXs/I3eb1TRVAuUHqz60VP5hPlTLZjuxTlBLXOYxzlRmrpX0HUxHcFMd+f8xjMrTs4osAdn80u4+U/1lLfv8ma3McYYY4wxxhhjjDHGGGOG/AWD6cpEDHuA9AAAAABJRU5ErkJggg==>

[image37]: <data:image/png;base64,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>