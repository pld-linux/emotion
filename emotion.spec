#
# Conditional build:
%bcond_without	gstreamer	# don't build gstreamer decoder
%bcond_without	xine		# don't build xine decoder
%bcond_without	static_libs	# don't build static library
#
%if !%{with gstreamer} && !%{with xine}
error at last one backend must be enabled
%endif
#
Summary:	Enlightenment Fundation Libraries - Emotion
Summary(pl):	Podstawowe biblioteki Enlightenmenta - Emotion
Name:		emotion
Version:	0.0.1.004
%define	_snap	20060625
Release:	2.%{_snap}.1
License:	BSD
Group:		X11/Libraries
#Source0:	http://enlightenment.freedesktop.org/files/%{name}-%{version}.tar.gz
Source0:	http://sparky.homelinux.org/snaps/enli/e17/libs/%{name}-%{_snap}.tar.bz2
# Source0-md5:	aa4f66fba709b4b08c2ed49eda196657
URL:		http://enlightenment.org/Libraries/Emotion/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	edje
BuildRequires:	edje-devel
%if %{with gstreamer}
BuildRequires:	gstreamer-cdio
BuildRequires:	gstreamer-devel >= 0.10.2
BuildRequires:	gstreamer-ffmpeg
BuildRequires:	gstreamer-plugins-base-devel >= 0.10.1
%endif
BuildRequires:	libtool
BuildRequires:	pkgconfig
%{?with_xine:BuildRequires:	xine-lib-devel >= 2:1.1.1}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Emotion is a Media Library.

%description -l pl
Emotion to biblioteka multimedialna.

%package devel
Summary:	Emotion header files
Summary(pl):	Pliki nag³ówkowe Emotion
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for Emotion.

%description devel -l pl
Pliki nag³ówkowe Emotion.

%package static
Summary:	Static Emotion library
Summary(pl):	Statyczna biblioteka Emotion
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static Emotion library.

%description static -l pl
Statyczna biblioteka Emotion.

%package decoder-gstreamer
Summary:	Emotion decoder using gstreamer
Summary(pl):	Dekoder Emotion u¿ywaj±cy gstreamera
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description decoder-gstreamer
Emotion decoder using gstreamer.

%description decoder-gstreamer -l pl
Dekoder Emotion u¿ywaj±cy gstreamera.

%package decoder-xine
Summary:	Emotion decoder using xine
Summary(pl):	Dekoder Emotion u¿ywaj±cy xine
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description decoder-xine
Emotion decoder using xine.

%description decoder-xine -l pl
Dekoder Emotion u¿ywaj±cy xine.

%prep
%setup -q -n %{name}

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{!?with_static_libs:--disable-static} \
	%{?without_gstreamer:--disable-gstreamer} \
	%{?without_xine:--disable-xine}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING COPYING-PLAIN README TODO
%attr(755,root,root) %{_bindir}/emotion_*
%attr(755,root,root) %{_libdir}/libemotion.so.*.*.*
%dir %{_libdir}/%{name}
%{_datadir}/%{name}

%if %{with gstreamer}
%files decoder-gstreamer
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/%{name}/emotion_decoder_gstreamer.so
%endif

%if %{with xine}
%files decoder-xine
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/%{name}/emotion_decoder_xine.so
%endif

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/emotion-config
%attr(755,root,root) %{_libdir}/libemotion.so
%{_libdir}/libemotion.la
%{_libdir}/%{name}/emotion_decoder_gstreamer.la
#%{_libdir}/%{name}/emotion_decoder_xine.la
%{_includedir}/Emotion*
%{_pkgconfigdir}/emotion.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libemotion.a
%endif
