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
   :emuName => "EVENT_EMU",
   :emuType => "MIX",
   :emuResourceType => "MIX",
   :emuStartTime => "now",
   :emuStopTime => "30",
   :distributions => {
	:name => "EVENT-1",
	:startTime =>"0",
	:minJobTime => "2",
	:distribution => {
			:href => "/distributions/event",
			:name => "event"},
	:emulator =>{
			:href => "/emulators/backfuzz",
			:name => "backfuzz"},
	:'emulator-params' =>{
			:resourceType =>"NET",
			:serverPort => "51889",
			:min => "100",
			:fuzzRange => "100",
			:protocol => "TCP",
			:timeDelay => "1",
			:salt => "5",
			:serverIP => "10.55.168.142"},
   },

   :log => {
	:enable => 1,
	:frequency => 3,
	:logLevel => "debug"
   }
 )
               
end
