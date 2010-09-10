%define		trac_ver	0.12
%define		plugin		tags
Summary:	A Tagging System for Trac
Name:		trac-plugin-%{plugin}
Version:	0.6
Release:	0.4
License:	BSD
Group:		Applications/WWW
# Source0Download:	http://trac-hacks.org/changeset/latest/tagsplugin/tags/0.6?old_path=/&filename=tagsplugin/tags/0.6&format=zip
Source0:	%{plugin}-%{version}.zip
# Source0-md5:	82c5dead1f61c82ea1f6a023ca612a77
Patch0:		pysqlite.patch
URL:		http://trac-hacks.org/wiki/TagsPlugin
BuildRequires:	python-devel
BuildRequires:	python-setuptools
BuildRequires:	rpm-pythonprov
Requires:	trac >= %{trac_ver}
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The TagsPlugin  implements both a generic tagging engine, and
frontends for the Wiki and ticket systems. An extra text entry box is
added to the Wiki edit page for tagging Wiki pages, and ticket fields
(you can configure which ones) are treated as tags for the ticket
system.

%prep
%setup -q -n %{plugin}plugin
%patch0 -p1

%build
cd %{plugin}/%{version}
%{__python} setup.py build
%{__python} setup.py egg_info

%install
rm -rf $RPM_BUILD_ROOT
cd %{plugin}/%{version}
%{__python} setup.py install \
	--single-version-externally-managed \
	--optimize 2 \
	--root=$RPM_BUILD_ROOT

%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ "$1" = "1" ]; then
	%banner -e %{name} <<-'EOF'
	To enable the %{plugin} plugin, add to conf/trac.ini:

	[components]
	trac%{plugin}.* = enabled
EOF
fi

%files
%defattr(644,root,root,755)
%{py_sitescriptdir}/trac%{plugin}
%{py_sitescriptdir}/TracTags-*.egg-info
