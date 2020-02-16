Feature: Processes subject line of webform from a queue and then outputs to queue

  Scenario:
    When the lambda is triggered with message that contains
      | post_code     | N16 8BR                                    |
      | body          | Please help me apply for new business visa |
      | first_name    | Tester                                     |
      | last_name     | Surname                                    |
      | email_address | tester.surname@gmail.com                   |
      | email_subject | Help me stay in country                    |
      | mp_ref        | R02834094                                  |
      | subject       | Visa                                       |
      | type          | Personal                                   |
    Then a message is published to the output topic that contains
      | post_code     | N16 8BR                                    |
      | body          | Please help me apply for new business visa |
      | first_name    | Tester                                     |
      | last_name     | Surname                                    |
      | email_address | tester.surname@gmail.com                   |
      | email_subject | Help me stay in country                    |
      | mp_ref        | R02834094                                  |
      | subject       | Visa                                       |
      | type          | Personal                                   |