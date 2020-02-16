# frozen_string_literal: true

class Hash
  def contains?(other)
    merge(other) == self
  end
end
