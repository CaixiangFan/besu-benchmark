# bpet

This repo provides a scripts to create a blockchain nodes cluster on Canada Compute (cc-rrg project), run benchmarks using HL Caliper, and automatically collect reports and logs after each test.

# Steps

1. Create a Besu cluster.

```
git clone https://github.com/CaixiangFan/bpet.git
cd bpet & create venv & install -r requirements.txt
source /home/ubuntu/gitrepo/bpet/venv/bin/activate
cd deploy & python create_instances.py
```

2. Run benchmark tests

```
cd ../caliper-benchmarks
python run_test.py
```
