#
# Conditional build:
%bcond_without	doc	# don't build doc
%bcond_with	tests	# do not perform "make test"
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define		module		xdis
%define		egg_name	xdis
%define		pypi_name	xdis
Summary:	Python cross-version byte-code disassembler and marshal routines
Name:		python-%{module}
Version:	4.1.2
Release:	3
License:	MIT
Group:		Libraries/Python
Source0:	https://files.pythonhosted.org/packages/source/x/%{module}/%{module}-%{version}.tar.gz
# Source0-md5:	8aca98d1837df4b0073fe1cacd65d91d
URL:		https://github.com/rocky/python-xdis/
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with python2}
BuildRequires:	python-nose >= 1.0
BuildRequires:	python-setuptools
%endif
%if %{with python3}
BuildRequires:	python3-nose >= 1.0
BuildRequires:	python3-setuptools
%endif
Requires:	python-setuptools
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Python dis module allows you to disassemble byte from the same
version of Python that you are running on. But what about bytecode
from different versions?

That's what this package is for. It can marshal load Python bytecodes
from different versions of Python. The command-line routine
pydisssemble will show disassembly output using Python 3.5 disassembly
conventions

It accepts bytecodes from Python version 2.3 to 3.5 or so. The code
requires Python 2.5 or later and has been tested on Python running
versions 2.6, 2.7, pypy-5.0.1, 3.2, 3.3, 3.4 and 3.5.

%package -n python3-%{pypi_name}
Summary:	Python cross-version byte-code disassembler and marshal routines
Group:		Libraries/Python
Requires:	python3-setuptools

%description -n python3-%{pypi_name}
The Python dis module allows you to disassemble byte from the same
version of Python that you are running on. But what about bytecode
from different versions?

That's what this package is for. It can marshal load Python bytecodes
from different versions of Python. The command-line routine
pydisssemble will show disassembly output using Python 3.5 disassembly
conventions

It accepts bytecodes from Python version 2.3 to 3.5 or so. The code
requires Python 2.5 or later and has been tested on Python running
versions 2.6, 2.7, pypy-5.0.1, 3.2, 3.3, 3.4 and 3.5.

%prep
%setup -q -n %{module}-%{version}

# Remove bundled egg-info
%{__rm} -r %{module}.egg-info

%build
%if %{with python2}
%py_build
%{?with_tests:%{__make} PYTHON=python check}
%endif

%if %{with python3}
%py3_build
%{?with_tests:%{__make} PYTHON=python3 check}
%endif

%install
rm -rf $RPM_BUILD_ROOT
%if %{with python2}
%py_install
%py_postclean
%{__mv} $RPM_BUILD_ROOT%{_bindir}/pydisasm{,-2}
%endif

%if %{with python3}
%py3_install
%{__mv} $RPM_BUILD_ROOT%{_bindir}/pydisasm{,-3}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc README.rst
%attr(755,root,root) %{_bindir}/pydisasm-2
%{py_sitescriptdir}/%{module}
%{py_sitescriptdir}/%{egg_name}-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-%{pypi_name}
%defattr(644,root,root,755)
%doc README.rst
%attr(755,root,root) %{_bindir}/pydisasm-3
%{py3_sitescriptdir}/%{module}
%{py3_sitescriptdir}/%{egg_name}-%{version}-py*.egg-info
%endif
