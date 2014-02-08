%define major	2
%define libname %mklibname %{name}_ %{major}
%define devname %mklibname -d %{name}

Summary:	Color Management Engine
Name:		lcms2
Version:	2.5
Release:	2
License:	MIT
Group:		Graphics
Url:		http://www.littlecms.com/
Source0:	http://www.littlecms.com/%{name}-%{version}.tar.gz
BuildRequires:	jpeg-devel
BuildRequires:	tiff-devel
BuildRequires:	pkgconfig(zlib)

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

%prep
%setup -q
%apply_patches

%build
autoreconf -fi
%configure2_5x \
	--disable-static \
	--program-suffix=2
%make

%install
%makeinstall_std

install -D -m 644 include/lcms2.h %{buildroot}%{_includedir}/lcms2.h
install -D -m 644 include/lcms2_plugin.h %{buildroot}%{_includedir}/lcms2_plugin.h

%files
%doc AUTHORS COPYING
%{_bindir}/*
%{_mandir}/man1/*

%files -n %{libname}
%{_libdir}/liblcms2.so.%{major}*

%files -n %{devname}
%doc doc/*.pdf
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/%{name}.pc

