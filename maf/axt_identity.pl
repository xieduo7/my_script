#!user/bin/perl -w
use strict;
use Getopt::Long;
my ($window,$str1,$str2,$box1,$box2,$container1,$container2,@dis);

my $ref=shift;
my $query=shift;
my $axtfile=shift;

my($match,$mismatch);
if($axtfile=~/\.gz$/){
        open IN,"gzip -dc $axtfile|" or die "Cannot open the file!\n";
}
else{
        open IN,"<",$axtfile or die "Cannot open the file!\n";
}
$/ ="\n\n";
while(<IN>){
	chomp;
	my @axt = split /\n/;
	my $len=length($axt[1]);
	my $str1=$axt[1];
	my $str2=$axt[2];
#	my();
	foreach(0..$len-1){
		my $base1=substr($str1,$_,1);
		my $base2=substr($str2,$_,1);
		if($base1 eq $base2){
			$match++;
		}
		else{
			$mismatch++;
		}
	}
	
}
my $identity=($match/($match+$mismatch));
#print "";
print "$ref\t$query\t$identity\n";
