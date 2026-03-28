// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

interface IEntryPoint {
    function handleOps(
        UserOperation[] calldata ops,
        address payable beneficiary
    ) external;
}

struct UserOperation {
    address sender;
    uint256 nonce;
    bytes initCode;
    bytes callData;
    uint256 callGasLimit;
    uint256 verificationGasLimit;
    uint256 preVerificationGas;
    uint256 maxFeePerGas;
    uint256 maxPriorityFeePerGas;
    bytes paymasterAndData;
    bytes signature;
}

contract SmartAccount {
    address public owner;
    mapping(address => bool) public sessionKeys;

    constructor(address _owner) {
        owner = _owner;
    }

    function addSessionKey(address key) external {
        require(msg.sender == owner, "not owner");
        sessionKeys[key] = true;
    }

    function revokeSessionKey(address key) external {
        require(msg.sender == owner, "not owner");
        sessionKeys[key] = false;
    }

    function validateSignature(
        bytes32 hash,
        bytes memory signature
    ) public view returns (bool) {
        address signer = recoverSigner(hash, signature);

        if (signer == address(0)) return false;
        if (signer == owner) return true;
        if (sessionKeys[signer]) return true;

        return false;
    }

    function recoverSigner(
        bytes32 hash,
        bytes memory sig
    ) internal pure returns (address) {
        (uint8 v, bytes32 r, bytes32 s) = split(sig);
        return ecrecover(hash, v, r, s);
    }

    function split(bytes memory sig)
        internal
        pure
        returns (uint8, bytes32, bytes32)
    {
        require(sig.length == 65, "invalid signature length");
        bytes32 r;
        bytes32 s;
        uint8 v;

        assembly {
            r := mload(add(sig, 32))
            s := mload(add(sig, 64))
            v := byte(0, mload(add(sig, 96)))
        }

        return (v, r, s);
    }
}
