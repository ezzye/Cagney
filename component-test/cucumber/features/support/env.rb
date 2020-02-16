# frozen_string_literal: true

require 'cucumber'
require 'rspec/matchers'
require 'fileutils'
require 'rest-assured'

BASE_DIR = File.expand_path('../../../..', File.dirname(__FILE__))
CUCUMBER_DIR = File.expand_path('../..', File.dirname(__FILE__))
TMP_DIR = File.expand_path('../../tmp', File.dirname(__FILE__))

Dir.mkdir TMP_DIR unless File.exist? TMP_DIR

AfterConfiguration do
  LOCAL_STACK = LocalStack.new
  BAD_MESSAGE_QUEUE = BMQ.new('BadMessageQueue')
  OUTPUT_TOPIC = SNS.new('OutputTopic')
  ISPY_TOPIC = SNS.new('IspyTopic')
end

After do |result|
  if @under_test && result.failed?
    puts 'STDOUT:'
    puts @under_test.stdout
  end
end

at_exit do
  LOCAL_STACK.kill
  FileUtils.rm_rf TMP_DIR
end
