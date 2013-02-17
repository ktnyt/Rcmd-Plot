#!/usr/local/bin/perl
use strict;

use CGI;
use CGI::Carp qw(fatalsToBrowser);

use Rcmd::Plot;

my $cgi = CGI->new();

my $chd   = $cgi->param("chd");
my $chs   = $cgi->param("chs");
my $cht   = $cgi->param("cht");
my $chif  = $cgi->param("chif");
my $chtt  = $cgi->param("chtt");
my $chxt  = $cgi->param("chxt");
my $chco  = $cgi->param("chco");
my $chls  = $cgi->param("chls");
my $chlt  = $cgi->param("chlt");
my $chdl  = $cgi->param("chdl");
my $chdlp = $cgi->param("chdlp");

my ( $width,  $height ) = split /[x,\/\| \t]/, $chs;
my ( $xlabel, $ylabel ) = split /[x,\/\| \t]/, $chxt;

my $jobid = time . substr( rand(10), -4 );

while ( -e "./graph/" . $jobid . ".png" ) {
    $jobid = time . substr( rand(10), -4 );
}

my $filename = "$jobid.png";

my $plot = Rcmd::Plot->new(
    data   => $chd,
    width  => $width,
    height => $height,
    ( title     => $chtt ) x !!($chtt),
    ( xlabel    => $xlabel ) x !!($xlabel),
    ( ylabel    => $ylabel ) x !!($ylabel),
    ( color     => $chco ) x !!($chco),
    ( linestyle => $chls ) x !!($chls),
    ( linetype  => $chlt ) x !!($chlt),
    ( legend    => $chdl ) x !!($chdl),
    ( legendpos => $chdlp ) x !!($chdlp),
    format   => "png",
    filename => "./graph/$filename"
);

if ( $cht eq "scat" ) {
    $plot->scat();
}

if ( $cht eq "bar" ) {
    $plot->bar();
}

if ( $cht eq "pie" ) {
    $plot->pie();
}

if ( $cht eq "box" ) {
    $plot->box();
}

if ( $cht eq "hist" ) {
    $plot->hist();
}

unless ( -e "./graph" ) {
    mkdir "graph", 0777 or die "$!:graph";
}

if ( -e "./graph/$filename" ) {
    chmod 777, "./graph/$filename";
    print "Location: http://localhost/~kotone/biochart/graph/$filename\n\r\n";
    exit;
}

print $cgi->header( -status => '400 Bad request' );
print $cgi->start_html( -title => 'Bad request' );
print $cgi->h1('400 Bad request');
print $cgi->p('A bad qualifier has been passed.');
print $cgi->end_html;