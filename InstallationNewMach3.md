# Installing New MaCh3 in cedar Compute Canada account

Instructions given by Daniel Barrow to follow the steps below:

```bash
mkdir NewMaCh3 && cd NewMaCh3
git clone git@github.com:/t2k-software/MaCh3 && cd MaCh3
git checkout T2K_Atmospherics
./setup_inputs.sh --ATM
```
`setup_inputs.sh` will take approximately 20 minutes.

Use the following setup bash file `Setup.sh` to set up the environment and load gcc, cmake, root, etc., which are prerequisites for installing MaCh3:

```bash
source /cvmfs/larsoft.opensciencegrid.org/spack-packages/setup-env.sh
spack load root@6.28.06
spack load gcc@12.2.0
spack load cmake

source /cvmfs/larsoft.opensciencegrid.org/spack-packages/opt/spack/linux-almalinux9-x86_64_v2/gcc-12.2.0/root-6.28.06-jhpj2jsdlwoxbvpnwmxvzkntrxcgw5of/bin/thisroot.sh
```
All Compute Canada clusters should have access to `cvmfs`.

```bash
source Setup.sh
```

Then you can check the following:

```bash
which root
```
Expected following root info:

```bash
/cvmfs/larsoft.opensciencegrid.org/spack-packages/opt/spack/linux-almalinux9-x86_64_v2/gcc-12.2.0/root-6.28.06-jhpj2jsdlwoxbvpnwmxvzkntrxcgw5of/bin/root
```

Check the versions of gcc, cmake, and root:

```bash
gcc --version
cmake --version
root-config --version
```

Expected versions:
```bash
cmake version 3.27.7
gcc (Spack GCC) 12.2.0
root 6.28/06
```

Now create a build directory:

```bash
mkdir build && cd build
```

Run cmake:

```bash
cmake .. -DCUDAProb3_ENABLED=ON
```
Check following CUDAProb3:
```bash
-- [INFO]: LOG LEVEL: INFO
-- CPM: MaCh3: Adding package NuOscillator@1.2.0 (v1.2.0)
-- [INFO]: NuOscillator Features:
-- [INFO]:      CUDAProb3: 1
-- [INFO]:      CUDAProb3Linear: 0
-- [INFO]:      Prob3ppLinear: 0
-- [INFO]:      ProbGPULinear: 0
-- [INFO]:      NuFASTLinear:  1
-- [INFO]:      OscProb: 0
-- [INFO]: Required variables being used:
-- [INFO]: 	Not using GPU
-- [INFO]: 	Using Multithreading with nThreads=64
-- [INFO]: Set compiler options: -g;-pedantic;-O3;-finline-limit=100000000;-fopenmp
-- CPM: MaCh3: NuOscillator: Adding package CUDAProb3@ (develop)
-- CPM: MaCh3: NuOscillator: Adding package NuFAST@1.0 (v1.0)
-- [INFO]: Compile options for MaCh3CompilerOptions: -g;-pedantic;-O3;-finline-limit=100000000;-fopenmp
-- [INFO]: Link libraries for MaCh3CompilerOptions: MaCh3CompileDefinitions;gomp
-- [INFO]: MaCh3 Features:
-- [INFO]:      DEBUG: FALSE
-- [INFO]:      MULTITHREAD: TRUE
-- [INFO]:      GPU: FALSE
-- [INFO]:      PYTHON: OFF
-- [INFO]:      LOW_MEMORY_STRUCTS: OFF
-- [INFO]:      Oscillator: CUDAProb3;NuFastLinear
-- [INFO]:      Fitter: MR2T2; PSO; Minuit2
-- [INFO]: Didn't find MaCh3, attempting to use built in MaCh3
-- [INFO]: CMAKE CXX Standard: 17
.
.
.
-- [INFO]:         ROOT_CONFIG_VERSION: 6.28/06
-- CPM: NIWG: Using local package toml11@3.7.1
-- [INFO]: NIWG CXX Standard: 17
-- [INFO]: MaCh3T2K Features:
-- [INFO]:      NIWG: TRUE
-- [INFO]:      PSYCHE: OFF
-- [INFO]:      T2KSK: TRUE
-- [INFO]:      SKDETCOV: FALSE
-- Configuring done (286.3s)
-- Generating done (40.9s)
-- Build files have been written to: /home/hadhikar/NewMaCh32/MaCh3/build
```
Run make install:

```bash
make install -j10
```

After the installation is finished, source all setup files in the build bin directory:

```bash
cd ..
source build/bin/setup.MaCh3.sh
source build/bin/setup.MaCh3T2K.sh
source build/bin/setup.NIWG.sh
```
Then create configs in the `configs/Samples/AtmosphericSamples/` directory:

```bash
cd configs/Samples/AtmosphericSamples/
python MakeConfigs.py
cd ../../../
```

Finally, run the SKEventRates executable in the MaCh3 directory to run `configs/AtmosphericJointFit.yaml`:

```bash
SKEventRates configs/AtmosphericJointFit.yaml
```

Submit job in cluster using sbatch:
```bash
#!/bin/bash
#SBATCH --time=03:00:00
#SBATCH --mail-user=h.adhikary@uw.edu.pl
#SBATCH --mail-type=ALL
#SBATCH --job-name=SKEventRates
#SBATCH --ntasks=1
#SBATCH --nodes=1
#SBATCH --mem-per-cpu=5G
#SBATCH --cpus-per-task=4
#SBATCH --gres=gpu:v100l:1
#SBATCH --account=def-blairt2k
cd /home/hadhikar/NewMaCh3v2/MaCh3
source Setup.sh
source build/bin/setup.MaCh3.sh
source build/bin/setup.MaCh3T2K.sh
source build/bin/setup.NIWG.sh
#export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK
export OMP_NUM_THREADS=12
SKEventRates configs/AtmosphericJointFit.yaml
```
Also git pull recent update and make install in build directory:

```bash
git pull
make install
```

Make change in configs/AtmosphericJointFit.yaml in #L4-L21 for simplification: 
```bash
SKSamples: ["configs/Samples/AtmosphericSamples/AtmSample_1.yaml",
           configs/Samples/AtmosphericSamples/AtmSample_2.yaml",
           configs/Samples/AtmosphericSamples/AtmSample_4.yaml",
           configs/Samples/AtmosphericSamples/AtmSample_5.yaml"]
```

Expected output:

```bash
SubGeV-elike-1dcy : 687.464
SubGeV-mulike-0dcy : 1265.19
SubGeV-mulike-1dcy : 5554.6
SubGeV-mulike-2dcy : 438.489
SubGeV-pi0like : 1501.81
MultiGeV-elike-nue : 199.869
MultiGeV-elike-nuebar : 1067.77
MultiGeV-mulike : 981.878
MultiRing-elike-nue : 1040.82
MultiRing-elike-nuebar : 1011.35
MultiRing-mulike : 2495.06
MultiRingOther-1 : 1204.96
PCStop : 342.758
PCThru : 1677.62
UpStop-mu : 749.828
UpThruNonShower-mu : 2590.32
UpThruShower-mu : 474.104
```
