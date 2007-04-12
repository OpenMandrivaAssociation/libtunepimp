%define major	5
%define libname	%mklibname tunepimp %major

%define build_plf 0
%{?_with_plf: %{expand: %%global build_plf 1}}
%if %build_plf
%define distsuffix plf
%endif

Name:	libtunepimp
Version:	0.5.3
Release:	%mkrel 2
Epoch: 1
Summary: A library for creating MusicBrainz enabled tagging applications
Source0:	ftp://ftp.musicbrainz.org/pub/musicbrainz/%{name}-%{version}.tar.bz2
License:	LGPL
Group:		System/Libraries
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
Url:		http://musicbrainz.org/doc/libtunepimp
BuildRequires:	libflac-devel
BuildRequires:	readline-devel
BuildRequires:	libmad-devel
BuildRequires:	oggvorbis-devel
BuildRequires:	libmusicbrainz-devel
BuildRequires:	libcurl-devel
BuildRequires:	libofa-devel
BuildRequires:	taglib-devel
BuildRequires:	libmpcdec-devel
BuildRequires:	python-devel
%if %build_plf
BuildRequires:	libmp4v2-devel
%endif

%description
The TunePimp library (also referred to as libtunepimp) is
a development library geared towards developers who wish
to create MusicBrainz enabled tagging applications. 

%if %build_plf
This package is in PLF as it may violate some MP4 patents.
%endif


#-----------------------------------------------------------

%package -n	tunepimp-utils
Summary:        A library for creating MusicBrainz enabled tagging applications
Group:          Sound
Obsoletes: %{_lib}tunepimp2-utils
Obsoletes: %{_lib}tunepimp5-utils

%description -n tunepimp-utils
This package contains %{name} tools

%files -n tunepimp-utils
%defattr(-,root,root)
%doc AUTHORS ChangeLog INSTALL README README.LGPL TODO
%{_bindir}/*

#-----------------------------------------------------------

%package -n	tunepimp-plugins
Summary: A library for creating MusicBrainz enabled tagging applications
Group: Sound
Obsoletes: %{_lib}tunepimp2-plugins
Obsoletes: %{_lib}tunepimp5-plugins

%description -n tunepimp-plugins
This package contains %{name} plugins

%files -n tunepimp-plugins
%defattr(-,root,root)
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
%if %build_plf
%{_libdir}/tunepimp/plugins/mp4.tpp
%endif

#-----------------------------------------------------------

%package -n	%{libname}
Summary:        A library for creating MusicBrainz enabled tagging applications
Group:          System/Libraries

%description -n	%{libname}
The TunePimp library (also referred to as libtunepimp) is
a development library geared towards developers who wish
to create MusicBrainz enabled tagging applications.

%post -p /sbin/ldconfig -n %{libname}
%postun -p /sbin/ldconfig -n %{libname}

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/*.so.%{major}*

#-----------------------------------------------------------

%package -n	%{libname}-devel
Summary:	Files needed for developing applications which use litunepimp
Group:		Development/C
Provides:	%{name}-devel = %{epoch}:%{version}-%{release}
Requires:	%{libname} = %{epoch}:%{version}-%{release}
Obsoletes: %{_lib}tunepimp2-devel
Obsoletes: %{_lib}tunepimp3-devel

%description -n	%{libname}-devel
The %{name}-devel package includes the header files and .so libraries
necessary for developing MusicBrainz enabled tagging applications.

If you are going to develop MusicBrainz enabled tagging 
applications you should install %{name}-devel. You'll also need 
to have the %name package installed.

%files -n %{libname}-devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/*.la

#-----------------------------------------------------------

%package -n	%{libname}-static-devel
Summary:        Static libraries for libtunepimp
Group:          Development/C
Provides:       %{name}-static-devel = %{version}-%{release}
Requires:       %{libname}-devel = %{epoch}:%{version}-%{release}

%description -n	%{libname}-static-devel
The %{name}-devel package includes the static libraries
necessary for developing MusicBrainz enabled tagging
applications using the %{name} library.

If you are going to develop MusicBrainz enabled tagging applications,
you should install %{name}-devel.  You'll also need to have the %name
package installed.

%files -n %{libname}-static-devel
%defattr(-,root,root)
%{_libdir}/*.a

%package -n	python-tunepimp
Summary:	Python binding to use libtunepimp
Group:		Development/Python
Requires:	python-ctypes
Requires:	%libname = %epoch:%version

%description -n python-tunepimp
Python binding to use libtunepimp.

%files -n python-tunepimp
%defattr(-,root,root)
%py_puresitedir/*

#-----------------------------------------------------------

%prep
%setup -q

%build
%configure2_5x
%make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std
cd python
python setup.py install --root=$RPM_BUILD_ROOT

%clean
rm -rf %buildroot





