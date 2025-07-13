// SPDX-License-Identifier: MIT
pragma solidity 0.8.17;

contract TrafficViolationSystem {
    address payable public authority;

    constructor(address payable _authority) {
        authority = _authority;  // Authority is passed in explicitly
    }

    struct Violation {
        string vehicleId;
        string trafficId;
        string violationType;
        string ipfsHash;
        uint256 timestamp;
        bool paid;
        string geolocation;
        string cameraId;
        uint256 penaltyAmount;
        address payable vehicleOwner;
    }

    mapping(bytes32 => Violation) public violations;
    mapping(address => uint256) public balances;

    event ViolationRecorded(bytes32 violationId, string vehicleId, uint256 penalty);
    event PenaltyPaid(bytes32 violationId, address payer, uint256 amount);

    function addViolation(
        string memory _vehicleId,
        string memory _trafficId,
        string memory _violationType,
        string memory _ipfsHash,
        uint256 _timestamp,
        string memory _geolocation,
        string memory _cameraId,
        address payable _vehicleOwner
    ) public payable returns (bytes32) {
        require(msg.value > 0, "Ether not sent");

        bytes32 violationId = keccak256(abi.encodePacked(_vehicleId, _timestamp));

        // ✅ Transfer the ETH to authority (NOT the caller anymore)
        authority.transfer(msg.value);

        violations[violationId] = Violation(
            _vehicleId,
            _trafficId,
            _violationType,
            _ipfsHash,
            _timestamp,
            true,
            _geolocation,
            _cameraId,
            msg.value,
            _vehicleOwner
        );

        emit ViolationRecorded(violationId, _vehicleId, msg.value);
        emit PenaltyPaid(violationId, _vehicleOwner, msg.value);

        return violationId;
    }

    function deposit() public payable {
        balances[msg.sender] += msg.value;
    }

    function getBalance(address _owner) public view returns (uint256) {
        return balances[_owner];
    }

    function checkBalance(address addr) public view returns (uint256) {
        return balances[addr];
    }
}
