# frozen_string_literal: true

require 'aws-sdk-sns'

SNS_ENDPOINT = 'http://localhost:4575'
SNS_CLIENT = Aws::SNS::Client.new(endpoint: SNS_ENDPOINT)

class SNS
  attr_reader :arn, :sqs

  def initialize(name)
    @arn = SNS_CLIENT.create_topic(name: name).topic_arn
    @sqs = SQS.new("#{name}Queue")
    subscribe(@sqs)
  end

  def subscribe(sqs)
    SNS_CLIENT.subscribe(
      topic_arn: @arn,
      protocol: 'sqs',
      endpoint: sqs.url,
      attributes: { RawMessageDelivery: 'true' }
    )
  end
end
