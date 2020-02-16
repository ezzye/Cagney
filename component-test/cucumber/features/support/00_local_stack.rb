# frozen_string_literal: true

class LocalStack
  def initialize
    @process = ProcessHelper::ProcessHelper.new

    @process.start(
        %w[pipenv run env SERVICES=sns,sqs,s3 LAMBDA_EXECUTOR=local localstack start --host],
      /Ready/,
      60
    )
  end

  def kill
    @process.kill
  end
end
