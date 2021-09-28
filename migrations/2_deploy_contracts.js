const EnergyCoin = artifacts.require("EnergyCoin");
const PaymentSettlement = artifacts.require("PaymentSettlement")
const PoolMarket = artifacts.require("PoolMarket");
// const SimpleStorage = artifacts.require('SimpleStorage')

module.exports = async function(deployer, network, accounts) {
  await deployer.deploy(EnergyCoin, "energycoin", "ec", 6, 1000, 2);
  const ecInstance = await EnergyCoin.deployed()
  await deployer.link(EnergyCoin, PaymentSettlement);
  await deployer.deploy(PaymentSettlement, ecInstance.address, {from: accounts[0]});
  const psInstance = await PaymentSettlement.deployed()
  await deployer.link(EnergyCoin, PoolMarket);
  await deployer.link(PaymentSettlement, PoolMarket);
  await deployer.deploy(PoolMarket, psInstance.address, ecInstance.address);
};
// module.exports = async function(deployer, network) {
//   await deployer.deploy(SimpleStorage,100)
// }
