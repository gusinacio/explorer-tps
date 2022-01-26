# BIG QUERY ETHEREUM

You can use those on the public dataset from bigquery: 

https://console.cloud.google.com/bigquery


## TOTAL GAS SPENT

```
SELECT DATE(block_timestamp) AS day,
SUM(cast(receipt_gas_used as BIGNUMERIC) * cast(gas_price as BIGNUMERIC)) as total_eth_spent,
SUM(cast(receipt_gas_used as BIGNUMERIC)) as total_gas

FROM bigquery-public-data.crypto_ethereum.transactions

WHERE CAST(EXTRACT(YEAR from block_timestamp) as string) = "2021"

GROUP BY day

ORDER BY day
```

## GAS USED BY SIDECHAIN

```
SELECT DATE(block_timestamp) AS day,
SUM(CASE When to_address IN UNNEST([LOWER("0xa0c68c638235ee32657e8f720a23cec1bfc77c77"),LOWER("0x401f6c983ea34274ec46f84d70b31c151321188b"), LOWER("0x2A88696e0fFA76bAA1338F2C74497cC013495922"), LOWER("0x86E4Dc95c7FBdBf52e33D563BbDB00823894C287")])  THEN receipt_gas_used ELSE 0 END) as total_gas_polygon,
SUM(CASE When to_address IN UNNEST([LOWER("0x4bf681894abec828b212c906082b444ceb2f6cf6"),LOWER("0xe969c2724d2448f1d1a6189d3e2aa1f37d5998c1"), LOWER("0x25ace71c97b33cc4729cf772ae268934f7ab5fa1"), LOWER("0xa88e220c7fc7f0d845d2624a5df1dfd6874b9a44"), LOWER("0x6786EB419547a4902d285F70c6acDbC9AefAdB6F"), LOWER("0xcd9d4988c0ae61887b075ba77f08cbfad2b65068"), LOWER("0x99c9fc46f92e8a1c0dec1b1747d010903e884be1"), LOWER("0x10e6593cdda8c58a1d0f14c5164b376352a55f2f"), LOWER("0xcd626E1328b41fCF24737F137BcD4CE0c32bc8d1"), LOWER("0x5E4e65926BA27467555EB562121fac00D24E9dD2"), LOWER("0xD16463EF9b0338CE3D73309028ef1714D220c024"), LOWER("0xb0ddFf09c4019e31960de11bD845E836078E8EbE"), LOWER("0xdE1FCfB0851916CA5101820A69b13a4E276bd81F"), LOWER("0x25ace71c97B33Cc4729CF772ae268934F7ab5fA1"), LOWER("0x99C9fc46f92E8a1c0deC1b1747d010903E884bE1"), LOWER("0xBe5dAb4A2e9cd0F27300dB4aB94BeE3A233AEB19")])  THEN receipt_gas_used ELSE 0 END) as total_gas_optimism,
SUM(CASE When to_address IN UNNEST([LOWER("0xaBEA9132b05A70803a4E85094fD0e1800777fBEF"),LOWER("0xda7357bBCe5e8C616Bc7B0C3C86f0C71c5b4EaBb"), LOWER("0x5140Cc54Bb876aBE1ba67d15AC66Ad2D42FDf46A"), LOWER("0x7C770595a2Be9A87CF49B35eA9bC534f1a59552D")])  THEN receipt_gas_used ELSE 0 END) as total_gas_zksync,
SUM(CASE When to_address IN UNNEST([LOWER("0x4aa42145Aa6Ebf72e164C9bBC74fbD3788045016")])  THEN receipt_gas_used ELSE 0 END) as total_gas_xdai,
SUM(CASE When to_address IN UNNEST([LOWER("0xd819E948b14cA6AAD2b7Ffd333cCDf732b129EeD")])  THEN receipt_gas_used ELSE 0 END) as total_gas_poa,
SUM(CASE When to_address IN UNNEST([LOWER("0x1a2a1c938ce3ec39b6d47113c7955baa9dd454f2")])  THEN receipt_gas_used ELSE 0 END) as total_gas_ronin,
SUM(CASE When to_address IN UNNEST([LOWER("0x4c6f947Ae67F572afa4ae0730947DE7C874F95Ef"),LOWER("0xC12BA48c781F6e392B49Db2E25Cd0c28cD77531A"),LOWER("0x4Dbd4fc535Ac27206064B68FfCf827b0A60BAB3f"),LOWER("0x72Ce9c846789fdB6fC1f34aC4AD25Dd9ef7031ef"),LOWER("0x011b6e24ffb0b5f5fcc564cf4183c5bbbc96d515"),LOWER("0xa3A7B6F88361F48403514059F1F16C8E78d60EeC"),LOWER("0x594393B6A6A46190dF3E479304bbC63572c6830a")])  THEN receipt_gas_used ELSE 0 END) as total_gas_arbitrum

FROM bigquery-public-data.crypto_ethereum.transactions

WHERE CAST(EXTRACT(YEAR from block_timestamp) as string) = "2021"

GROUP BY day

ORDER BY day
```

## GAS USED BY SIDECHAIN WITHOUT DEPOSITS/WITHDRAWALS

```
SELECT DATE(block_timestamp) AS day,
SUM(CASE When to_address IN UNNEST([LOWER("0x86E4Dc95c7FBdBf52e33D563BbDB00823894C287")])  THEN receipt_gas_used ELSE 0 END) as total_gas_polygon,
SUM(CASE When to_address IN UNNEST([LOWER("0x4bf681894abec828b212c906082b444ceb2f6cf6"),LOWER("0xe969c2724d2448f1d1a6189d3e2aa1f37d5998c1"), LOWER("0xa88e220c7fc7f0d845d2624a5df1dfd6874b9a44"), LOWER("0x6786EB419547a4902d285F70c6acDbC9AefAdB6F"), LOWER("0x5E4e65926BA27467555EB562121fac00D24E9dD2"), LOWER("0xBe5dAb4A2e9cd0F27300dB4aB94BeE3A233AEB19")])  THEN receipt_gas_used ELSE 0 END) as total_gas_optimism,
SUM(CASE When to_address IN UNNEST([LOWER("0xaBEA9132b05A70803a4E85094fD0e1800777fBEF"),LOWER("0xda7357bBCe5e8C616Bc7B0C3C86f0C71c5b4EaBb"), LOWER("0x5140Cc54Bb876aBE1ba67d15AC66Ad2D42FDf46A"), LOWER("0x7C770595a2Be9A87CF49B35eA9bC534f1a59552D")]) AND input NOT LIKE "0x2d2da806%" AND input NOT LIKE "0xe17376b5%" AND input NOT LIKE "0xb0705b42%"  THEN receipt_gas_used ELSE 0 END) as total_gas_zksync,
0 as total_gas_xdai,
0 as total_gas_poa,
SUM(CASE When to_address IN UNNEST([LOWER("0x1a2a1c938ce3ec39b6d47113c7955baa9dd454f2")]) AND input NOT LIKE "0x85eb3a35%" AND input NOT LIKE "0xeee3f07a%" AND input NOT LIKE "0x993e1c42%"  THEN receipt_gas_used ELSE 0 END) as total_gas_ronin,
SUM(CASE When to_address IN UNNEST([LOWER("0x4c6f947Ae67F572afa4ae0730947DE7C874F95Ef"),LOWER("0xC12BA48c781F6e392B49Db2E25Cd0c28cD77531A")])  THEN receipt_gas_used ELSE 0 END) as total_gas_arbitrum

FROM `bigquery-public-data.crypto_ethereum.transactions`

WHERE CAST(EXTRACT(YEAR from block_timestamp) as string) = "2021"

GROUP BY day

ORDER BY day
```

## ETHEREUM USAGE PERCENTAGE

```
SELECT

DATE(timestamp) as day,

SUM(cast(gas_used as BIGNUMERIC)) as total_gas_used,

SUM(cast(gas_limit as BIGNUMERIC)) as total_gas_limit,

AVG(gas_limit) as avg_gas_limit,

(SUM(cast(gas_used as BIGNUMERIC)) / SUM(cast(gas_limit as BIGNUMERIC)) ) as usage_percentage

FROM bigquery-public-data.crypto_ethereum.blocks 

WHERE CAST(EXTRACT(YEAR from timestamp) as string) = "2021"

GROUP BY day

ORDER BY day
```
