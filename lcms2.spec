# lcms2 is used by wine
%ifarch %{x86_64}
%bcond_without compat32
%endif

%define major 2
%define libname %mklibname %{name}_ %{major}
%define devname %mklibname -d %{name}
%define lib32name %mklib32name %{name}_ %{major}
%define dev32name %mklib32name -d %{name}

Summary:	Color Management Engine
Name:		lcms2
Version:	2.12
Release:	1
License:	MIT
Group:		Graphics
Url:		http://www.littlecms.com/
Source0:	https://sourceforge.net/projects/lcms/files/lcms/%{version}/%{name}-%{version}.tar.gz
BuildRequires:	jbig-devel
BuildRequires:	tiff-devel
BuildRequires:	pkgconfig(zlib)
%if %{with compat32}
BuildRequires:	devel(libtiff)
BuildRequires:	devel(libz)
%endif

%description
LittleCMS intends to be a small-footprint, speed optimized color management
engine in open source form. LCMS2 is the current version of LCMS, and can be
parallel installed with the original (deprecated) lcms.

%package -n %{libname}
Summary:	Libraries for LittleCMS
Group:		System/Libraries

%description -n %{libname}
This package provides the shared lcms2 library.

%package -n %{devname}
Summary:	Development files for LittleCMS
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{devname}
Development files for LittleCMS2.

%if %{with compat32}
%package -n %{lib32name}
Summary:	Libraries for LittleCMS (32-bit)
Group:		System/Libraries

%description -n %{lib32name}
This package provides the shared lcms2 library.

%package -n %{dev32name}
Summary:	Development files for LittleCMS (32-bit)
Group:		Development/C
Requires:	%{devname} = %{version}-%{release}
Requires:	%{lib32name} = %{version}-%{release}

%description -n %{dev32name}
Development files for LittleCMS2.
%endif

%prep
%autosetup -p1
export CONFIGURE_TOP="$(pwd)"
%if %{with compat32}
mkdir build32
cd build32
%configure32 --program-suffix=2
cd ..
%endif

mkdir build
cd build
%configure --program-suffix=2
cd ..

sed -i -e 's,define CMSEXPORT,define CMSEXPORT __attribute__((visibility("default"))),g' include/lcms2.h

%build
%if %{with compat32}
%make_build -C build32
%endif
%make_build -C build

%install
%if %{with compat32}
%make_install -C build32
%endif
%make_install -C build

# No need to re-export from an external application...
sed -i -e 's,define CMSEXPORT __attribute__((visibility("default"))),define CMSEXPORT,g' include/lcms2.h

install -D -m 644 include/lcms2.h %{buildroot}%{_includedir}/lcms2.h
install -D -m 644 include/lcms2_plugin.h %{buildroot}%{_includedir}/lcms2_plugin.h

%files
%doc AUTHORS COPYING
%{_bindir}/*
%{_mandir}/man1/*

%files -n %{libname}
%{_libdir}/liblcms2.so.%{major}*

%files -n %{devname}
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/%{name}.pc

%if %{with compat32}
%files -n %{lib32name}
%{_prefix}/lib/liblcms2.so.%{major}*

%files -n %{dev32name}
%{_prefix}/lib/*.so
%{_prefix}/lib/pkgconfig/%{name}.pc
%endif
