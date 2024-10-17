# Can't mix clang (C/C++) and gcc (fortran) when using LTO
#global _disable_lto 1

%define major 1
%define libname %mklibname rsb
%define devname %mklibname rsb -d

Summary:	A parallel sparse matrix computations library for the Recursive Sparse Blocks format
Name:		librsb
Version:	1.3.0.2
Release:	1
License:	zlib with acknowledgement
Group:		System/Libraries
URL:		https://librsb.sourceforge.net
Source0:	https://downloads.sourceforge.net/librsb/%{name}-%{version}.tar.gz

BuildRequires:	doxygen
BuildRequires:	help2man
BuildRequires:	gcc-gfortran
BuildRequires:	pkgconfig(gsl)
BuildRequires:	pkgconfig(libtirpc) 
BuildRequires:	pkgconfig(hwloc)
BuildRequires:	pkgconfig(zlib)

%description
librsb is a library for sparse matrix computations featuring the Recursive
Sparse Blocks (RSB) matrix format. This format allows cache efficient and
multi-threaded (that is, shared memory parallel) operations on large sparse
matrices. The most common operations necessary to iterative solvers are
available, e.g.: matrix-vector multiplication, triangular solution,
rows/columns scaling, diagonal extraction / setting, blocks extraction, norm
computation, formats conversion. The RSB format is especially well suited
for symmetric and transposed multiplication variants. Most numerical kernels
code is auto generated, and the supported numerical types can be chosen by
the user at build time.

librsb implements the Sparse BLAS standard, as specified in the BLAS Forum
documents.

#----------------------------------------------------------------------------

%package -n %{libname}
Summary:	A parallel sparse matrix computations library for the Recursive Sparse Blocks format
Group:		System/Libraries

%description -n %{libname}
librsb is a library for sparse matrix computations featuring the Recursive
Sparse Blocks (RSB) matrix format. This format allows cache efficient and
multi-threaded (that is, shared memory parallel) operations on large sparse
matrices. The most common operations necessary to iterative solvers are
available, e.g.: matrix-vector multiplication, triangular solution,
rows/columns scaling, diagonal extraction / setting, blocks extraction, norm
computation, formats conversion. The RSB format is especially well suited
for symmetric and transposed multiplication variants. Most numerical kernels
code is auto generated, and the supported numerical types can be chosen by
the user at build time.

librsb implements the Sparse BLAS standard, as specified in the BLAS Forum
documents.

%files -n %{libname}
%license COPYING
%{_libdir}/%{name}.so*

#----------------------------------------------------------------------------

%package -n %{devname}
Summary:	A parallel sparse matrix computations library for the Recursive Sparse Blocks format
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}

%description -n %{devname}
Headers and development files for %{name}.

%files -n %{devname}
%license COPYING
%doc AUTHORS ChangeLog README README.md
%{_bindir}/rsbench
%{_bindir}/librsb-config
%{_includedir}/*
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/%{name}.pc
%{_mandir}/man1/*.1*
%{_mandir}/man3/*.3*
%_docdir/%name/examples

#----------------------------------------------------------------------------

%prep
%autosetup -p1

%build
# Can't mix clang (C/C++) and gcc (fortran) when using LTO
export CC=gcc
export CXX=g++

# (mandian) avoid %%before_configure failure
%set_build_flags
./configure \
	CFLAGS="%optflags -Wno-unused -O3" \
	CXXFLAGS="%optflags -Wno-unused -O3" \
	LDFLAGS="%ldflags `pkgconf --libs libtirpc`" \
	--with-memhinfo=L3:16/64/8192K,L2:16/64/2048K,L1:8/64/16K \
	--libdir=%{_libdir} \
	--prefix=%{_prefix} \
	--docdir="%_docdir/%name" \
	--disable-static \
	--enable-doc-build \
	--enable-extra-patches \
	--enable-fortran-module-install \
	--enable-matrix-types=blas \
	--enable-pkg-config-install \
	--with-hwloc \
	--with-zlib=-lz \
	--without-rpm
%make_build

%install
%make_install

# install docs by hand
rm -f %{buildroot}%{_docdir}/%{name}/{AUTHORS,README,README.md}

