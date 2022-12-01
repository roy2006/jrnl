# Copyright © 2012-2022 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

Feature: Delete a tag from a journal
    Scenario Outline: Delete tag from hournal
        Given we use the config "<config_file>"
        When we run "jrnl -1"
        Then the output should contain "@tag"
        When we run "jrnl --delete-tag tag" 
        When we run "jrnl -2 "
        Then the output should not contain "@tag"
        And the output should contain "@othertag"
            
        Examples: Configs
        | config_file | 
        | config_file_for_tags.yaml |


