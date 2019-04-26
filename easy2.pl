#!/usr/bin/perl

# RITSEC Demos Week 13
# Easy 2

# Get input and check if it is valid
print "Enter the caesar cipher (letters only): ";
my $caesar = lc(<STDIN>);
chomp $caesar;
exit 0 if ($caesar eq "");

# Set up the initial shift
$shift=0;

while($shift != 26){

    # Split up the string
    $text=$_;
    $text =~ s/\r?\n$//;
    @characters=split(//, $caesar);
    $string="";

    foreach $character(@characters){
        $asciinum=ord($character);
        #perform the shift
        if(($asciinum+$shift)<=122){
            $string=$string . chr($asciinum+$shift);
        }
        else{$string=$string . chr($asciinum+$shift-122+96)};
    }

    # print the string
    print "$shift : $string\n";

    # increment the shift and restart
    $shift+=1;
}
