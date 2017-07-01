%define major	5
%define libname	%mklibname tunepimp %major
%define devname	%mklibname tunepimp -d
%define _disable_rebuild_configure 1

Summary:	A library for creating MusicBrainz enabled tagging applications
Name:		libtunepimp
Epoch:		1
Version:	0.5.3
Release:	30
License:	GPLv2+
Group:		System/Libraries
Url:		http://musicbrainz.org/doc/libtunepimp
Source0:	ftp://ftp.musicbrainz.org/pub/musicbrainz/%{name}-%{version}.tar.bz2
Patch0:		tunepimp-0.5.3-build-fix.patch
Patch1:		tunepimp-0.5.3-gcc43.patch
Patch2:		tunepimp-0.5.3-libtool.patch
Patch3:		libtunepimp-0.5.3-new-libmp4v2.patch
Patch4:		libtunepimp-0.5.3-gcc44.patch
Patch5:		libtunepimp-0.5.3-curl-7.26.patch
Patch6:		libtunepimp-automake-1.13.patch
Patch7:		libtunepimp-0.5.3-taglib-detection.patch

BuildRequires:	libmpcdec-devel
BuildRequires:	libmp4v2-devel >= 2.0
BuildRequires:	libtool-devel
BuildRequires:	readline-devel
BuildRequires:	pkgconfig(flac)
BuildRequires:	pkgconfig(libmusicbrainz)
BuildRequires:	pkgconfig(libcurl)
BuildRequires:	pkgconfig(libofa)
BuildRequires:	pkgconfig(mad)
BuildRequires:	pkgconfig(python2)
BuildRequires:	pkgconfig(taglib)
BuildRequires:	pkgconfig(vorbis)

%description
The TunePimp library (also referred to as libtunepimp) is
a development library geared towards developers who wish
to create MusicBrainz enabled tagging applications. 

%package -n	tunepimp-utils
Summary:	A library for creating MusicBrainz enabled tagging applications
Group:		Sound

%description -n tunepimp-utils
This package contains %{name} tools

%files -n tunepimp-utils
%doc AUTHORS ChangeLog INSTALL README README.LGPL TODO
%{_bindir}/*

%package -n	tunepimp-plugins
Summary:	A library for creating MusicBrainz enabled tagging applications
Group:		Sound

%description -n tunepimp-plugins
This package contains %{name} plugins

%files -n tunepimp-plugins
%dir %{_libdir}/tunepimp/
%dir %{_libdir}/tunepimp/plugins/
%{_libdir}/tunepimp/plugins/flac.tpp
%{_libdir}/tunepimp/plugins/mp3.tpp
%{_libdir}/tunepimp/plugins/mpc.tpp
%{_libdir}/tunepimp/plugins/speex.tpp
%{_libdir}/tunepimp/plugins/tta.tpp
%{_libdir}/tunepimp/plugins/vorbis.tpp
%{_libdir}/tunepimp/plugins/wav.tpp
%{_libdir}/tunepimp/plugins/wma.tpp
%{_libdir}/tunepimp/plugins/wv.tpp

%package -n	%{libname}
Summary:	A library for creating MusicBrainz enabled tagging applications
Group:		System/Libraries

%description -n	%{libname}
The TunePimp library (also referred to as libtunepimp) is
a development library geared towards developers who wish
to create MusicBrainz enabled tagging applications.

%files -n %{libname}
%{_libdir}/libtunepimp.so.%{major}*

%package -n	%{devname}
Summary:	Files needed for developing applications which use litunepimp
Group:		Development/C
Provides:	%{name}-devel = %{EVRD}
Requires:	%{libname} = %{EVRD}

%description -n	%{devname}
The %{name}-devel package includes the header files and .so libraries
necessary for developing MusicBrainz enabled tagging applications.

If you are going to develop MusicBrainz enabled tagging 
applications you should install %{name}-devel. You'll also need 
to have the %{name} package installed.

%files -n %{devname}
%{_includedir}/*
%{_libdir}/*.so

%package -n	python-tunepimp
Summary:	Python binding to use libtunepimp
Group:		Development/Python
Requires:	python-ctypes
Requires:	%{libname} = %{EVRD}
BuildRequires:	python-devel

%description -n python-tunepimp
Python binding to use libtunepimp.

%files -n python-tunepimp
%py2_puresitedir/*

%prep
%setup -q
%apply_patches

# Doesn't build and won't get fixed
sed -i -e 's, mp4,,' plugins/Makefile.am
sed -i -e 's,mp4v2,mp4v3,' configure.in

autoreconf -fi

%build
%configure \
	--with-included-ltdl=no \
	--with-ltdl-include=%{_includedir} \
	--with-ltdl-lib=%{_libdir} \
	--disable-static

%make

%install
%makeinstall_std

cd python
%{__python2} setup.py install --root=%{buildroot}

# Create symlink for current version includes
cd %{buildroot}%{_includedir}
ln -sf tunepimp-0.%major tunepimp

