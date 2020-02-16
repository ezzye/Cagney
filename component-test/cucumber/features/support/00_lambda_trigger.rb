# frozen_string_literal: true

class LambdaTrigger
  def initialize(event)
    File.write("#{TMP_DIR}/aws_lambda_msg", event.to_json)
    @process = ProcessHelper::ProcessHelper.new(print_lines: true)
    @process.start(LambdaTrigger.command, 'END RequestId', 30)
  end

  def stdout
    @process.get_log(:out).join
  end

  def self.command
    [
      'pipenv', 'run', 'env',
      "ISPY_TOPIC_ARN=#{ISPY_TOPIC.arn}",
      "OUTPUT_TOPIC_ARN=#{OUTPUT_TOPIC.arn}",
      "BAD_MESSAGE_QUEUE_URL=#{BAD_MESSAGE_QUEUE.url}",
      'INPUT_QUEUE_ARN=arn:aws:sqs:eu-west-1:000000000000:InputQueue',
      "SQS_ENDPOINT=#{SQS_ENDPOINT}",
      "SNS_ENDPOINT=#{SNS_ENDPOINT}",
      'python-lambda-local', '-l', BASE_DIR, "#{BASE_DIR}/src/cagney.py", "#{TMP_DIR}/aws_lambda_msg"
    ]
  end
end