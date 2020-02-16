# frozen_string_literal: true

class BMQ < SQS
  def receive(timeout: 10)
    rslt = super(timeout: timeout)
    parse_xml_body(rslt)
    rslt
  end
end

def parse_xml_body(message)
  xml_str = message[:body]
  message[:body] = BadMessage.new(xml_str)
end

class BadMessage
  attr_reader :body, :component, :stacktrace, :description, :source_queue

  def initialize(xml_str)
    doc = Nokogiri::XML(xml_str)
    @body = doc.at_xpath('//body').content
    @component = doc.at_xpath('//component').content
    @stacktrace = doc.at_xpath('//stacktrace').content
    @description = doc.at_xpath('//description').content
    @source_queue = doc.at_xpath('//sourceQueue').content
  end
end
