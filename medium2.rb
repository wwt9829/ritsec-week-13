require 'socket'
require 'timeout'

# RITSEC Demos Week 13
# Medium 2

$rhost = ARGV[0]
$min_port = ARGV[1]
$max_port = ARGV[2]

begin
  if (Integer $min_port) <= (Integer $max_port)
    $scan_range = ((Integer $min_port)..(Integer $max_port)).to_a
  else
    puts "Error: Invalid range."
    exit
  end
rescue ArgumentError
  puts "Error: Invalid range."
  exit
end

def scanport(port)
  s = Socket.new Socket::AF_INET, Socket::SOCK_STREAM
  begin
    sockaddr = Socket.pack_sockaddr_in(port, $rhost)
  rescue
    puts "Error: Failed to resolve target."
    exit
  end
  Timeout::timeout(10) do
      begin
        @result = s.connect(sockaddr)
      rescue
        return false
      end
  end
  if @result == 0
    return true
  else
    return false
  end
end

puts "Beginning scan...\n\n"

$scan_range.each do |port|
  if scanport(port)
    puts "Port " + port.to_s + ": Open"
  end
end

puts "\nScan complete."
