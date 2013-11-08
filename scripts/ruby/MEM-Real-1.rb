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
   :emuName => "MEM_REAL_EMU",
   :emuType => "TIME",
   :emuResourceType => "MEM",
   :emuStartTime => "now",
   :emuStopTime => "60",
   :distributions => {
	:name => "MEM-real",
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
			:resourceType => "MEM",
			:malloclimit => "4095",
			:memSleep => "0"},
   },
   :log => {
	:enable => 0,
	:frequency => 3,
	:logLevel => "debug"
   }
 )
               
end
