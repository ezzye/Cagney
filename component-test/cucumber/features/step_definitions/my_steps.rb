When(/^the lambda is triggered with web email message that contains$/) do |table|
  # table is a table.hashes.keys # => [:post_code, :N16 8BR]
  body = table.rows_hash.to_json
  @message_id = SecureRandom.uuid
  sns_message = generate_sns_message(body, message_id: @message_id)
  event = SqsEvent.new.put_record(sns_message.to_json)
  @under_test = LambdaTrigger.new(event)
end

Then(/^a message is published to the output topic that contains$/) do |table|
  sns_message = OUTPUT_TOPIC.sqs.receive
  expect(sns_message.message_id).not_to be(nil)
  actual = JSON.parse(sns_message['body'], symbolize_names: true)
  expected = table.rows_hash.symbolize_keys
  expect(actual).to eq(expected)
end
