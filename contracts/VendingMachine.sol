// SPDX-License-Identifier: MIT
pragma solidity >=0.6.0 <0.9.0;

contract VendingMachine {
    address public owner;
    mapping(address => uint) public donutBalances;

    constructor() public {
        owner = msg.sender;
        donutBalances[address(this)] = 100; 
    }

    function getVendingMachineDonutsBalance() public view returns (uint) {
        return donutBalances[address(this)];
    }

    function restock(uint amount) public {
        require(msg.sender == owner, "only the owner can restock this machine.");
        donutBalances[address(this)] += amount;
    }    

    function purchase(uint amount) public payable{
        require(donutBalances[address(this)] >= amount, "not enought donuts to fulfill request");
        require(msg.value >= amount * 2 ether, "insufficient funds");
        donutBalances[address(this)] -= amount;
        donutBalances[msg.sender] += amount;
        if(msg.value > amount *2 ether)
        {
            payable(msg.sender).transfer(msg.value - (amount*2 ether));
        }
    }
}