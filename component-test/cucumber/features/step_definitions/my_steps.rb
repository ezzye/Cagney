When(/^the lambda is triggered with web email message that contains$/) do |table|
  # table is a table.hashes.keys # => [:post_code, :N16 8BR]
  body = table.rows_hash.symbolize_keys
  @message_id = SecureRandom.uuid
  # Make event
  event = SqsEvent.new.put_record(body.to_json, message_id: @message_id)
  # Trigger Lambda
  @under_test = LambdaTrigger.new(event)
end

Then(/^a message is published to the output topic that contains$/) do |table|
  sns_message = OUTPUT_TOPIC.sqs.receive
  expect(sns_message.message_id).not_to be(nil)
  actual = JSON.parse(sns_message['body'], symbolize_names: true)
  expected = table.rows_hash.symbolize_keys
  expect(actual).to eq(expected)
end
