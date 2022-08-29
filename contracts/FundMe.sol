// SPDX-License-Identifier: MIT
pragma solidity >=0.6.0 <0.9.0;

import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";


contract FundMe {
    //$50
    uint256 minimumUSD = 50 * 10 ** 18;

    address public owner;
    address[] public funders;

    // constructor() {
    //     owner = msg.sender;
    // }

    function setowner(address account) public {
        owner = account;
    }

    modifier onlyOwner {
        _;
        require(msg.sender == owner, "Error! Only the owner can call this method");
    }

    mapping(address => uint256) public addressToAmountFunded;

    function fund() public payable {
        require(getConversionRate(msg.value) >= minimumUSD, "You need to spend at least $50 in ETH!");
        addressToAmountFunded[msg.sender] += msg.value;
        funders.push(msg.sender);
    }

    function withdraw() onlyOwner public payable{
        payable(msg.sender).transfer(address(this).balance);
        for(uint256 i=0; i<funders.length; i++)
        {
            addressToAmountFunded[funders[i]] = 0;
        }
        funders = new address[](0);
    }

    function getVersion() public view returns(uint256) {
        AggregatorV3Interface versionFeed =  AggregatorV3Interface(0xD4a33860578De61DBAbDc8BFdb98FD742fA7028e);
        return versionFeed.version();
    }

    function getPrice() public view returns(uint256) {
        AggregatorV3Interface priceFeed = AggregatorV3Interface(0xD4a33860578De61DBAbDc8BFdb98FD742fA7028e);
        (,int256 answer,,,) = priceFeed.latestRoundData();
        return uint256(answer * 10000000000);
    }

    function getConversionRate(uint256 ethAmount) public view returns(uint256) {
        uint256 ethPrice = getPrice();
        return (ethPrice * ethAmount) / 1000000000000000000;
    } 
}