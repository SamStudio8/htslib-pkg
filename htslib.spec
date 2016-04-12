Name:           htslib
Version:        1.3
Release:        1%{?dist}
Summary:        C library for high-throughput sequencing data formats

# The entire source code is MIT except cram/ which is Modified-BSD
License:        MIT and BSD
URL:            http://www.htslib.org
Source0:        %{name}-%{version}.tar.gz

BuildRequires:	glibc-common, zlib-devel, ncurses

%description
HTSlib is an implementation of a unified C library for accessing common file
formats, such as SAM, CRAM and VCF, used for high-throughput sequencing data,
and is the core library used by samtools and bcftools.

%package        tools
Summary:        Additional htslib-based tools
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    tools
Includes the popular tabix indexer, which indexes both .tbi and .csi formats,
the htsfile identifier tool, and the bgzip compression utility.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q


%build
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
%make_install prefix=/usr libdir=/usr/lib64
make install-so %{?_smp_mflags} prefix=/usr libdir=/usr/lib64 DESTDIR=%{buildroot}
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%doc
%{_libdir}/*.so.*
%{_libdir}/*.so


%files devel
%doc
%{_includedir}/*
%{_libdir}/libhts.a
%{_libdir}/pkgconfig/htslib.pc
%{_mandir}/man5/faidx.5.gz
%{_mandir}/man5/sam.5.gz
%{_mandir}/man5/vcf.5.gz

%files tools
%{_bindir}/bgzip
%{_bindir}/htsfile
%{_bindir}/tabix
%{_mandir}/man1/htsfile.1.gz
%{_mandir}/man1/tabix.1.gz


%changelog
* Tue Apr 12 2016 makerpm
- 
