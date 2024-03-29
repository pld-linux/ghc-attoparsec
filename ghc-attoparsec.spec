#
# Conditional build:
%bcond_without	prof	# profiling library
#
%define		pkgname	attoparsec
Summary:	Fast combinator parsing for bytestrings
Summary(pl.UTF-8):	Szybki kombinator analizujący łańcuchy bajtów
Name:		ghc-%{pkgname}
Version:	0.13.2.4
Release:	2
License:	BSD
Group:		Development/Languages
#Source0Download: http://hackage.haskell.org/package/attoparsec
Source0:	http://hackage.haskell.org/package/%{pkgname}-%{version}/%{pkgname}-%{version}.tar.gz
# Source0-md5:	bbef0323147aaa59caccd5cb1289e719
URL:		http://hackage.haskell.org/package/attoparsec
BuildRequires:	ghc >= 6.12.3
BuildRequires:	ghc-array
BuildRequires:	ghc-base >= 3
BuildRequires:	ghc-bytestring
BuildRequires:	ghc-containers
BuildRequires:	ghc-deepseq
BuildRequires:	ghc-scientific >= 0.3.1
BuildRequires:	ghc-text >= 0.11.1.5
%if %{with prof}
BuildRequires:	ghc-prof >= 6.12.3
BuildRequires:	ghc-array-prof
BuildRequires:	ghc-base-prof >= 3
BuildRequires:	ghc-bytestring-prof
BuildRequires:	ghc-containers-prof
BuildRequires:	ghc-deepseq-prof
BuildRequires:	ghc-scientific-prof >= 0.3.1
BuildRequires:	ghc-text-prof >= 0.11.1.5
%endif
BuildRequires:	rpmbuild(macros) >= 1.608
%requires_eq	ghc
Requires(post,postun):	/usr/bin/ghc-pkg
Requires:	ghc-array
Requires:	ghc-base >= 3
Requires:	ghc-bytestring
Requires:	ghc-containers
Requires:	ghc-deepseq
Requires:	ghc-scientific >= 0.3.1
Requires:	ghc-text >= 0.11.1.5
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# debuginfo is not useful for ghc
%define		_enable_debug_packages	0

# don't compress haddock files
%define		_noautocompressdoc	*.haddock

%description
A fast parser combinator library, aimed particularly at dealing
efficiently with network protocols and complicated text/binary file
formats.

%description -l pl.UTF-8
Biblioteka szybkiego kombinatora analizatorów, przeznaczona
szczególnie do efektywnej obsługi protokołów sieciowych oraz
skomplikowanych formatów plików tekstowo-binarnych.

%package prof
Summary:	Profiling %{pkgname} library for GHC
Summary(pl.UTF-8):	Biblioteka profilująca %{pkgname} dla GHC
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	ghc-array-prof
Requires:	ghc-base-prof >= 3
Requires:	ghc-bytestring-prof
Requires:	ghc-containers-prof
Requires:	ghc-deepseq-prof
Requires:	ghc-scientific-prof >= 0.3.1
Requires:	ghc-text-prof >= 0.11.1.5

%description prof
Profiling %{pkgname} library for GHC. Should be installed when
GHC's profiling subsystem is needed.

%description prof -l pl.UTF-8
Biblioteka profilująca %{pkgname} dla GHC. Powinna być zainstalowana
kiedy potrzebujemy systemu profilującego z GHC.

%package doc
Summary:	HTML documentation for %{pkgname} ghc package
Summary(pl.UTF-8):	Dokumentacja w formacie HTML dla pakietu ghc %{pkgname}
Group:		Documentation

%description doc
HTML documentation for %{pkgname} ghc package.

%description doc -l pl.UTF-8
Dokumentacja w formacie HTML dla pakietu ghc %{pkgname}.

%prep
%setup -q -n %{pkgname}-%{version}

%build
runhaskell Setup.lhs configure -v2 \
	%{?with_prof:--enable-library-profiling} \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libexecdir} \
	--docdir=%{_docdir}/%{name}-%{version}

runhaskell Setup.lhs build
runhaskell Setup.lhs haddock --executables

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d

runhaskell Setup.lhs copy --destdir=$RPM_BUILD_ROOT

# work around automatic haddock docs installation
%{__rm} -rf %{name}-%{version}-doc
cp -a $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version} %{name}-%{version}-doc
%{__rm} -rf $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

runhaskell Setup.lhs register \
	--gen-pkg-config=$RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%ghc_pkg_recache

%postun
%ghc_pkg_recache

%files
%defattr(644,root,root,755)
%doc LICENSE README.markdown 
%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSattoparsec-%{version}-*.so
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSattoparsec-%{version}-*.a
%exclude %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSattoparsec-%{version}-*_p.a
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Attoparsec
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Attoparsec/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Attoparsec/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Attoparsec/ByteString
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Attoparsec/ByteString/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Attoparsec/ByteString/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Attoparsec/Internal
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Attoparsec/Internal/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Attoparsec/Internal/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Attoparsec/Text
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Attoparsec/Text/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Attoparsec/Text/*.dyn_hi

%if %{with prof}
%files prof
%defattr(644,root,root,755)
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSattoparsec-%{version}-*_p.a
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Attoparsec/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Attoparsec/ByteString/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Attoparsec/Internal/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Attoparsec/Text/*.p_hi
%endif

%files doc
%defattr(644,root,root,755)
%doc %{name}-%{version}-doc/*
