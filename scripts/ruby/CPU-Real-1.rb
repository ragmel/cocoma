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
   :emuName => "CPU_REAL_EMU",
   :emuType => "TIME",
   :emuResourceType => "CPU",
   :emuStartTime => "now",
   :emuStopTime => "60",
   :distributions => {
	:name => "CPU-real",
	:startTime =>"0",
	:minJobTime => "2",
	:distribution => {
			:href => "/distributions/real_trace",
			:name => "real_trace"},
	:trace => ENV['COCOMA'] + "/extra_tobe_fixed/real-trace_1.txt",
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
