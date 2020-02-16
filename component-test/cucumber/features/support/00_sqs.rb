# frozen_string_literal: true

require 'aws-sdk-sqs'

SQS_ENDPOINT = 'http://localhost:4576'
SQS_CLIENT = Aws::SQS::Client.new(endpoint: SQS_ENDPOINT)

class SQS
  attr_reader :url, :messages

  def initialize(name)
    @url = SQS_CLIENT.create_queue(queue_name: name).queue_url
    @messages = []
  end

  def receive(timeout: 10)
    result = _receive(timeout: timeout)
    if result.empty?
      nil
    elsif result.size == 1
      @messages.append(result[0])
      result[0]
    else
      raise 'Impossible error: Found more than 1 message'
    end
  end

  def _receive(timeout: 10)
    SQS_CLIENT.receive_message(
      queue_url: @url,
      max_number_of_messages: 1,
      wait_time_seconds: timeout,
      attribute_names: ['All']
    ).messages
  end

  def self.reset
    RestClient.delete(SQS_ENDPOINT)
  end
end
