#
# Conditional build:
%bcond_without	prof	# profiling library
#
%define		pkgname	attoparsec
Summary:	Fast combinator parsing for bytestrings
Summary(pl.UTF-8):	Szybki kombinator analizujący łańcuchy bajtów
Name:		ghc-%{pkgname}
Version:	0.10.4.0
Release:	1
License:	BSD
Group:		Development/Languages
#Source0Download: http://hackage.haskell.org/package/attoparsec
Source0:	http://hackage.haskell.org/package/%{pkgname}-%{version}/%{pkgname}-%{version}.tar.gz
# Source0-md5:	2b9ec5768797e8c649bf36efa9ef97e2
URL:		http://hackage.haskell.org/package/attoparsec
BuildRequires:	ghc >= 6.12.3
%{?with_prof:BuildRequires:	ghc-prof}
BuildRequires:	ghc-text >= 0.11.1.5
%{?with_prof:BuildRequires:	ghc-text-prof >= 0.11.1.5}
BuildRequires:	rpmbuild(macros) >= 1.608
%requires_releq	ghc
Requires(post,postun):	/usr/bin/ghc-pkg
Requires:	ghc-text >= 0.11.1.5
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# debuginfo is not useful for ghc
%define		_enable_debug_packages	0

# don't compress haddoc files
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
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/HSattoparsec-%{version}.o
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSattoparsec-%{version}.a
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/*.hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Attoparsec
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Attoparsec/*.hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Attoparsec/ByteString
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Attoparsec/ByteString/*.hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Attoparsec/Internal
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Attoparsec/Internal/*.hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Attoparsec/Text
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Attoparsec/Text/*.hi

%if %{with prof}
%files prof
%defattr(644,root,root,755)
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSattoparsec-%{version}_p.a
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Attoparsec/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Attoparsec/ByteString/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Attoparsec/Internal/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Attoparsec/Text/*.p_hi
%endif

%files doc
%defattr(644,root,root,755)
%doc %{name}-%{version}-doc/*
