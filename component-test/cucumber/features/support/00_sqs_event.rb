# frozen_string_literal: true

class SqsEvent < Hash
  def initialize
    self[:Records] = []
  end

  def put_record(body, message_id: SecureRandom.uuid)
    self[:Records].append(
      body: body,
      messageId: message_id
    )
    self
  end
end

def generate_sns_message(internal_message, message_id: SecureRandom.uuid)
  {
    Type: 'Notification',
    Message: internal_message,
    MessageId: message_id
  }
end
