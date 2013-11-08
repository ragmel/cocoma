require 'rubygems'
require 'restfully'
require 'logger'


session = Restfully::Session.new(
 :configuration_file => ENV['COCOMA'] + "/scripts/api.cocoma.yml"

)

session.logger.level = Logger::INFO

emulation = nil

begin
 emulation = session.root.emulations.submit(
   :emuName => "NET_EMU",
   :emuType => "TIME",
   :emuResourceType => "NET",
   :emuStartTime => "now",
   :emuStopTime => "30",

   :distributions => {
	:name => "NET-1",
	:startTime =>"0",
	:duration => "30",
	:granularity => "10",
	:minJobTime => "2",
	:distribution => {
			:href => "/distributions/linear",
			:name => "linear"},
	:startLoad => "1",
	:stopLoad => "100",
	:emulator =>{
			:href => "/emulators/iperf",
			:name => "iperf"},
	:'emulator-params' =>{
			:resourceType =>"NET",
			:serverPort => "51889",
			:serverIP => "10.55.168.142",
			:packetType => "UDP"}
   },

   :log => {
	:enable => 1,
	:frequency => 3,
	:logLevel => "debug"
   }
 )
               
end
