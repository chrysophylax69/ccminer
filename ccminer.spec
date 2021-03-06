%define gittag0 %{version}-tpruvot

# Disable annobin
%undefine _annotated_build

Name:           ccminer
Version:        2.2.5
Release:        2%{?dist}
Summary:        CUDA miner project
License:        GPLv2 and GPLv3
URL:            https://github.com/tpruvot/%{name}

Source0:        https://github.com/tpruvot/%{name}/archive/%{gittag0}.tar.gz#/%{name}-%{gittag0}.tar.gz
# https://github.com/tpruvot/ccminer/pull/61
Patch0:         https://patch-diff.githubusercontent.com/raw/tpruvot/ccminer/pull/61.patch#/ccminer-2.2.5-monero-v7.patch

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  cuda-devel
BuildRequires:  jansson-devel
BuildRequires:  libcurl-devel >= 7.15.2
BuildRequires:  libstdc++-devel
BuildRequires:  libtool
BuildRequires:  mpir-devel
BuildRequires:  openssl-devel

%if 0%{?fedora}
BuildRequires:  cuda-gcc-c++
%endif

%description
This is a CUDA accelerated mining application which handles:
    Decred (Blake256 14-rounds - 180 bytes)
    HeavyCoin & MjollnirCoin
    FugueCoin
    GroestlCoin & Myriad-Groestl
    Lbry Credits
    JackpotCoin (JHA)
    QuarkCoin family & AnimeCoin
    TalkCoin
    DarkCoin and other X11 coins
    Chaincoin and Flaxscript (C11)
    Saffroncoin blake (256 14-rounds)
    BlakeCoin (256 8-rounds)
    Qubit (Digibyte, ...)
    Luffa (Joincoin)
    Keccak (Maxcoin)
    Pentablake (Blake 512 x5)
    1Coin Triple S
    Neoscrypt (FeatherCoin)
    Revolver (X11evo)
    Scrypt and Scrypt:N
    Scrypt-Jane (Chacha)
    Sibcoin (sib)
    Skein (Skein + SHA)
    Signatum (Skein cubehash fugue Streebog)
    Tribus (JH, keccak, simd)
    Woodcoin (Double Skein)
    Vanilla (Blake256 8-rounds - double sha256)
    Vertcoin Lyra2RE
    Ziftrcoin (ZR5)
    Boolberry (Wild Keccak)
    Monero (Cryptonight)
    Aeon (Cryptonight-lite)

%prep
%autosetup -p1 -n %{name}-%{gittag0}

# Make sure to pick up CUDA headers
sed -i -e 's|-I$with_cuda/include|-I$with_cuda/include/cuda|g' configure.ac

%if 0%{?fedora}
# Use compat GCC for building
sed -i -e 's|nvcc"|nvcc -ccbin /usr/bin/cuda-g++ -Xcompiler -fPIC"|g' configure.ac
%endif

%build
autoreconf -vif

%if 0%{?fedora}
export CXX=cuda-g++
%endif

%if 0%{?fedora} >= 27
export CFLAGS=`echo %{build_cflags} -fPIC | sed -e 's/-fstack-clash-protection -mcet -fcf-protection//g'`
export CXXFLAGS=`echo %{build_cxxflags} -fPIC | sed -e 's/-fstack-clash-protection -mcet -fcf-protection//g'`
export FFLAGS=`echo %{build_fflags} -fPIC | sed -e 's/-fstack-clash-protection -mcet -fcf-protection//g'`
export FCFLAGS=`echo %{build_fflags} -fPIC | sed -e 's/-fstack-clash-protection -mcet -fcf-protection//g'`
%else
export CXXFLAGS="%{optflags} -fPIC"
%endif

%configure --with-cuda=%{_prefix} --with-nvml=%{_libdir}

%make_build

%install
%make_install

%files
%license LICENSE.txt
%doc README.txt
%{_bindir}/ccminer

%changelog
* Wed May 09 2018 Simone Caronni <negativo17@gmail.com> - 2.2.5-2
- Add Monero V7 patch.
- Momentarily disable annobin plugin.
- Remove unsupported compiler flags.

* Mon Apr 23 2018 Simone Caronni <negativo17@gmail.com> - 2.2.5-1
- Update to 2.2.5.

* Mon Jan 15 2018 Simone Caronni <negativo17@gmail.com> - 2.2.4-1
- Update to 2.2.4.

* Thu Dec 14 2017 Simone Caronni <negativo17@gmail.com> - 2.2.3-1
- Update to 2.2.3.

* Wed Nov 01 2017 Simone Caronni <negativo17@gmail.com> - 2.2.2-1
- Update to 2.2.2.
- Override compiler with cuda-gcc for CUDA 9 on Fedora.
- Disable Compute architecture 2.x for CUDA 9.

* Sun Sep 10 2017 Simone Caronni <negativo17@gmail.com> - 2.2.1-1
- Update to 2.2.1.

* Mon Jul 24 2017 Simone Caronni <negativo17@gmail.com> - 2.1-1
- Update to 2.1.

* Tue May 30 2017 Simone Caronni <negativo17@gmail.com> - 2.0-2
- Update to 2.0 final.

* Fri Apr 28 2017 Simone Caronni <negativo17@gmail.com> - 2.0-1
- Update to latest release.
- Use GCC 5.3 on Fedora.

* Sun Nov 15 2015 Simone Caronni <negativo17@gmail.com> - 1.7.0-1
- Update to 1.7.0.

* Thu Oct 01 2015 Simone Caronni <negativo17@gmail.com> - 1.6.6-1
- Update to 1.6.6; rebuilt with CUDA 7.5.

* Wed Jul 29 2015 Simone Caronni <negativo17@gmail.com> - 1.6.5-1.C11
- Update to 1.6.5-C11.
- Switch to updated packaging guidelines for Github.

* Sat Apr 11 2015 Simone Caronni <negativo17@gmail.com> - 1.6.0-1.git.4426700
- Update to 1.6.0.

* Tue Jan 20 2015 Simone Caronni <negativo17@gmail.com> - 1.5.1-1.git.9adb7d7
- Update to 1.5.1.

* Wed Dec 10 2014 Simone Caronni <negativo17@gmail.com> - 1.5.0-1.git.70743eb
- -Update to latest 1.5.0 snapshot.

* Mon Nov 10 2014 Simone Caronni <negativo17@gmail.com> 1.4.7-1.git.2ab1e37
- First build.
