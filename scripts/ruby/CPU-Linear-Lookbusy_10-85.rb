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
   :emuName => "CPU_EMU",
   :emuType => "TIME",
   :emuResourceType => "CPU",
   :emuStartTime => "now",
   :emuStopTime => "60",
   :distributions => {
	:name => "CPU-increase",
	:startTime =>"0",
	:duration =>"60",        
	:granularity =>"10",
	:minJobTime => "2",
	:distribution => {
			:href => "/distributions/linear",
			:name => "linear"},
	:startLoad => "10",
	:stopLoad => "85",
	:emulator =>{
			:href => "/emulators/lookbusy",
			:name => "lookbusy"},
	:'emulator-params' =>{
			:resourceType =>"CPU",
			:ncpus => "0"}
   },
   :log => {
	:enable => 0,
	:frequency => 3,
	:logLevel => "debug"
   }
 )
               
end
