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

Run make install:

```bash
make install -j10
```

After the installation is finished, source all setup files in the build bin directory:

```bash
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
