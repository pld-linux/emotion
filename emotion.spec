Summary:	Enlightenment Fundation Libraries - emotion
Name:		emotion
Version:	0.0.1
%define	_snap	20050105
Release:	0.%{_snap}.0.1
License:	BSD
Group:		X11/Libraries
#Source0:	http://dl.sourceforge.net/enlightenment/%{name}-%{version}.tar.gz
Source0:	ftp://ftp.sparky.homelinux.org/pub/e17/%{name}-%{version}-%{_snap}.tar.gz
# Source0-md5:	1b5ff54c3da9b30f3b4d2d7d412b69b2
URL:		http://enlightenment.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	edje-devel
BuildRequires:	libtool
BuildRequires:	xine-lib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Emotion is a Media Library.

%package devel
Summary:	Emotion headers, documentation and test programs
Group:		Development/Libraries
Requires:	%{name} = %{version}
Requires:	xine-lib-devel

%description devel
Headers, test programs and documentation for Emotion.

%package static
Summary:	Static libraries
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}

%description static
Static libraries.

%prep
%setup -q -n %{name}

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure
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
%doc AUTHORS COPYING* README
%attr(755,root,root) %{_libdir}/libemotion.so.*
%attr(755,root,root) %{_bindir}/emotion_*
%{_datadir}/%{name}

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/emotion-config
%{_pkgconfigdir}/emotion.pc
%attr(755,root,root) %{_libdir}/libemotion.so
%{_libdir}/libemotion.la
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/emotion_decoder_xine.la
%attr(755,root,root) %{_libdir}/emotion/emotion_decoder_xine.so
%attr(755,root,root) %{_libdir}/xine/plugins/*/xineplug_vo_out_emotion.so
%{_libdir}/xine/plugins/*/xineplug_vo_out_emotion.la
%{_includedir}/Emotion*

%files static
%defattr(644,root,root,755)
%{_libdir}/libemotion.a
%{_libdir}/emotion/emotion_decoder_xine.a
%{_libdir}/xine/plugins/*/xineplug_vo_out_emotion.a
