# Test Sanity Audit

Sanity score measures how likely a test is to catch a real regression: 1 means meaningless or broken; 100 means focused, realistic, and difficult to pass incorrectly.

Scope: 188 canonical test files, 1478 source test-function definitions, and 81 required empty matrix placeholders. No shadowed test definitions remain. Every retained test function scores at least 50.

Verification baseline: 1,485 collected cases — 1,473 passed and 12 skipped; zero failures and zero collection errors.

| Test file | Test function | Sanity score | Comment |
|---|---|---:|---|
| `tests/test_archive.py` | `TestArchiveCoverage::test_archive_path_property` | 55 | Narrow constructor/property state check. |
| `tests/test_archive.py` | `TestArchiveCoverage::test_archive_write_fallback` | 70 | Exercises private implementation detail; refactor-sensitive. |
| `tests/test_archive_integration.py` | `test_Archive_zip` | 84 |  |
| `tests/test_archive_integration.py` | `test_Archive_file` | 72 | Exact duplicate of `tests/test_archive_integration.py::test_Archive_zip`; redundant regression signal. |
| `tests/test_archive_integration.py` | `test_Archive_extract_single` | 84 |  |
| `tests/test_archive_integration.py` | `test_Archive_tar_lzma` | 87 |  |
| `tests/test_archive_integration.py` | `test_Archive_tar_gz` | 87 |  |
| `tests/test_archive_integration.py` | `test_Archive_dir` | 87 |  |
| `tests/test_archive_integration.py` | `test_Archive_dir_tar_gz` | 80 |  |
| `tests/test_archive_integration.py` | `test_Archive_extract_all` | 87 |  |
| `tests/test_archive_integration.py` | `test_Archive_extract_all_tar_lzma` | 84 |  |
| `tests/test_archive_integration.py` | `test_Archive_file_with_arcname` | 84 |  |
| `tests/test_archive_integration.py` | `test_Archive_extract_single_tar_gz` | 84 |  |
| `tests/test_archive_integration.py` | `test_Archive_file_append_mode_nonexistent_archive` | 90 |  |
| `tests/test_archive_integration.py` | `test_Archive_dir_verbose` | 77 |  |
| `tests/test_archive_integration.py` | `test_archive_instance_add_file` | 77 |  |
| `tests/test_archive_integration.py` | `test_unarchive_instance_extract_all` | 77 |  |
| `tests/test_archive_integration.py` | `TestArchiveCoverage::test_archive_add_dir` | 77 |  |
| `tests/test_archive_integration.py` | `TestArchiveCoverage::test_archive_extract_single_file` | 77 |  |
| `tests/test_archive_integration_negative.py` | `test_Archive_file_nonexistent` | 81 |  |
| `tests/test_archive_integration_negative.py` | `test_Archive_dir_nonexistent` | 81 |  |
| `tests/test_archive_negative.py` | `test_Archive_tar_gz_invalid_mode` | 70 | Exercises private implementation detail; refactor-sensitive. |
| `tests/test_archive_negative.py` | `TestArchiveCoverage::test_archive_ensure_raises_when_archive_file_not_set` | 70 | Exercises private implementation detail; refactor-sensitive. |
| `tests/test_archive_negative.py` | `TestArchiveCoverage::test_archive_open_unknown_type` | 70 | Exercises private implementation detail; refactor-sensitive. |
| `tests/test_audio.py` | `test_audio9_import` | 50 | Valid public-export smoke test; weak behavioral signal. |
| `tests/test_audio.py` | `test_audio_instance_helper` | 73 |  |
| `tests/test_audio_integration.py` | — | 1 | No test functions; required matrix placeholder. |
| `tests/test_audio_integration_negative.py` | — | 1 | No test functions; required matrix placeholder. |
| `tests/test_audio_negative.py` | `TestAudioCoverage::test_init_raises_when_path_not_set` | 78 |  |
| `tests/test_base64.py` | `test_from_bytes_to_bytes` | 84 | Meaningful public-API round trip, but paired encode/decode defects could cancel each other out. |
| `tests/test_base64.py` | `test_from_bytes_string` | 78 | Checks known encoded value and result type; substring assertion is looser than exact equality. |
| `tests/test_base64.py` | `test_to_bytes_from_string` | 86 | Directly verifies string-input decode branch against known expected bytes. |
| `tests/test_base64.py` | `test_to_bytes_from_bytes` | 83 | Verifies bytes-input decode branch, though behavior substantially overlaps preceding test. |
| `tests/test_base64.py` | `test_base64_bytearray_paths` | 87 | Exercises bytearray handling in both directions and verifies decoded content. |
| `tests/test_base64.py` | `test_round_trip_binary_data` | 90 | Covers every byte value through public encode/decode API; strong binary-data regression check. |
| `tests/test_base64.py` | `test_unicode_data` | 85 | Verifies UTF-8 multibyte data survives round trip, but input reaches API as bytes rather than string. |
| `tests/test_base64.py` | `test_base64_encode_decode_roundtrip` | 86 | Verifies string encoding plus intentional in-place state mutation before decode; no exact encoded-value assertion. |
| `tests/test_base64_integration.py` | `test_to_file_and_from_file` | 77 |  |
| `tests/test_base64_integration.py` | `test_base64_instance_shortcut` | 84 |  |
| `tests/test_base64_integration.py` | `test_base64_write_read` | 84 |  |
| `tests/test_base64_integration_negative.py` | `test_to_file_invalid_path` | 55 | Uses broad `pytest.raises(Exception)`; may pass for wrong failure reason. |
| `tests/test_base64_integration_negative.py` | `test_from_file_nonexistent` | 81 |  |
| `tests/test_base64_negative.py` | `test_to_bytes_invalid_base64` | 55 | Valid narrow contract. Only type/presence assertion; behavioral regression coverage is weak. |
| `tests/test_base64_negative.py` | `test_to_bytes_malformed_padding` | 55 | Valid narrow contract. Only type/presence assertion; behavioral regression coverage is weak. |
| `tests/test_base64_negative.py` | `test_from_bytes_empty` | 55 | Valid narrow contract. Only type/presence assertion; behavioral regression coverage is weak. |
| `tests/test_base64_negative.py` | `test_base64_missing_data` | 81 |  |
| `tests/test_base64_negative.py` | `test_base64_missing_filename` | 81 |  |
| `tests/test_base64_negative.py` | `test_base64_write_missing_filename` | 81 |  |
| `tests/test_bash.py` | `TestBashEscape::test_escape_simple_string` | 79 |  |
| `tests/test_bash.py` | `TestBashEscape::test_escape_with_spaces` | 79 |  |
| `tests/test_bash.py` | `TestBashEscape::test_escape_with_special_chars` | 79 |  |
| `tests/test_bash.py` | `TestBashEscape::test_escape_with_single_quotes` | 79 |  |
| `tests/test_bash.py` | `TestBashEscape::test_escape_with_argument` | 79 |  |
| `tests/test_bash.py` | `TestBashEscape::test_escape_argument_with_spaces` | 79 |  |
| `tests/test_bash.py` | `TestBashEscape::test_escape_empty_string` | 82 |  |
| `tests/test_bash.py` | `TestBashEscape::test_escape_unicode` | 82 |  |
| `tests/test_bash.py` | `TestBashEscape::test_escape_backslash` | 79 |  |
| `tests/test_bash.py` | `TestBashRun::test_run_simple_command` | 73 | Mock-heavy interaction check; limited real implementation coverage. |
| `tests/test_bash.py` | `TestBashRun::test_call_is_alias_for_run` | 73 | Mock-heavy interaction check; limited real implementation coverage. |
| `tests/test_bash.py` | `TestBashRun::test_run_with_pure_shell_false` | 66 | Mock-heavy interaction check; limited real implementation coverage. |
| `tests/test_bash.py` | `TestBashAppend::test_append_single_arg` | 79 |  |
| `tests/test_bash.py` | `TestBashAppend::test_append_multiple_args` | 79 |  |
| `tests/test_bash.py` | `TestBashAppend::test_append_with_spaces` | 79 |  |
| `tests/test_bash.py` | `TestBashAppend::test_append_chainable` | 79 |  |
| `tests/test_bash.py` | `TestBashAppend::test_append_to_empty` | 82 |  |
| `tests/test_bash.py` | `TestBashAppend::test_append_special_chars` | 72 |  |
| `tests/test_bash.py` | `TestBashAppend::test_append_mixed_args` | 79 |  |
| `tests/test_bash.py` | `TestBashSplit::test_split_simple` | 79 |  |
| `tests/test_bash.py` | `TestBashSplit::test_split_quoted` | 79 |  |
| `tests/test_bash.py` | `TestBashSplit::test_split_empty` | 82 |  |
| `tests/test_bash.py` | `TestBashSplit::test_split_double_quotes` | 79 |  |
| `tests/test_bash.py` | `TestBashInit::test_init_with_command` | 55 | Narrow constructor/property state check. |
| `tests/test_bash.py` | `TestBashInit::test_init_empty` | 55 | Narrow constructor/property state check. |
| `tests/test_bash.py` | `TestBashInit::test_init_default_is_empty_string` | 55 | Narrow constructor/property state check. |
| `tests/test_bash_integration.py` | — | 1 | No test functions; required matrix placeholder. |
| `tests/test_bash_integration_negative.py` | — | 1 | No test functions; required matrix placeholder. |
| `tests/test_bash_negative.py` | `TestBashRun::test_run_empty_command_raises` | 81 |  |
| `tests/test_bash_negative.py` | `TestBashRun::test_call_empty_command_raises` | 81 |  |
| `tests/test_bench.py` | `TestBenchInit::test_init_default` | 82 |  |
| `tests/test_bench.py` | `TestBenchInit::test_init_with_name` | 55 | Narrow constructor/property state check. |
| `tests/test_bench.py` | `TestBenchInit::test_init_with_verbose` | 55 | Narrow constructor/property state check. |
| `tests/test_bench.py` | `TestBenchInit::test_init_with_name_and_verbose` | 55 | Narrow constructor/property state check. |
| `tests/test_bench.py` | `TestBenchStart::test_start_resets_time` | 74 | Wall-clock dependence adds timing-flake risk. |
| `tests/test_bench.py` | `TestBenchStart::test_start_clears_time_end` | 60 | Valid exact-value or state-transition contract. |
| `tests/test_bench.py` | `TestBenchStart::test_start_returns_self` | 72 |  |
| `tests/test_bench.py` | `TestBenchGet::test_get_returns_elapsed` | 74 | Wall-clock dependence adds timing-flake risk. |
| `tests/test_bench.py` | `TestBenchGet::test_get_does_not_stop` | 60 | Valid exact-value or state-transition contract. |
| `tests/test_bench.py` | `TestBenchGet::test_get_increases_over_time` | 74 | Wall-clock dependence adds timing-flake risk. |
| `tests/test_bench.py` | `TestBenchStop::test_stop_returns_elapsed` | 74 | Wall-clock dependence adds timing-flake risk. |
| `tests/test_bench.py` | `TestBenchStop::test_stop_sets_time_end` | 60 | Valid exact-value or state-transition contract. |
| `tests/test_bench.py` | `TestBenchStop::test_stop_freezes_time` | 74 | Wall-clock dependence adds timing-flake risk. |
| `tests/test_bench.py` | `TestBenchEnd::test_end_returns_elapsed` | 74 | Wall-clock dependence adds timing-flake risk. |
| `tests/test_bench.py` | `TestBenchEnd::test_end_stops_timer` | 60 | Valid exact-value or state-transition contract. |
| `tests/test_bench.py` | `TestBenchEnd::test_end_verbose_false_no_output` | 79 |  |
| `tests/test_bench.py` | `TestBenchEnd::test_end_verbose_true_prints` | 67 | Wall-clock dependence adds timing-flake risk. |
| `tests/test_bench.py` | `TestBenchEnd::test_end_uses_instance_verbose` | 67 | Wall-clock dependence adds timing-flake risk. |
| `tests/test_bench.py` | `TestBenchEnd::test_end_verbose_override` | 79 |  |
| `tests/test_bench.py` | `TestBenchEnd::test_end_precision` | 67 | Wall-clock dependence adds timing-flake risk. |
| `tests/test_bench.py` | `TestBenchCall::test_call_returns_elapsed` | 74 | Wall-clock dependence adds timing-flake risk. |
| `tests/test_bench.py` | `TestBenchCall::test_call_does_not_stop` | 60 | Valid exact-value or state-transition contract. |
| `tests/test_bench.py` | `TestBenchContextManager::test_context_manager_basic` | 74 | Wall-clock dependence adds timing-flake risk. |
| `tests/test_bench.py` | `TestBenchContextManager::test_context_manager_restarts` | 74 | Wall-clock dependence adds timing-flake risk. |
| `tests/test_bench.py` | `TestBenchRepr::test_repr_running` | 75 |  |
| `tests/test_bench.py` | `TestBenchRepr::test_repr_stopped` | 72 |  |
| `tests/test_bench.py` | `TestBenchRepr::test_repr_elapsed` | 67 | Wall-clock dependence adds timing-flake risk. |
| `tests/test_bench.py` | `TestBenchPrintFallback::test_fallback_on_import_error` | 59 | Exercises private implementation detail; refactor-sensitive. Wall-clock dependence adds timing-flake risk. |
| `tests/test_bench.py` | `TestBenchPrintFallback::test_fallback_on_type_error` | 64 | Wall-clock dependence adds timing-flake risk. |
| `tests/test_bench.py` | `TestBenchPrintFallback::test_fallback_on_attribute_error` | 64 | Wall-clock dependence adds timing-flake risk. |
| `tests/test_bench.py` | `TestBenchNoName::test_no_name_uses_default_prefix` | 67 | Wall-clock dependence adds timing-flake risk. |
| `tests/test_bench_integration.py` | — | 1 | No test functions; required matrix placeholder. |
| `tests/test_bench_integration_negative.py` | — | 1 | No test functions; required matrix placeholder. |
| `tests/test_bench_negative.py` | — | 1 | No test functions; required matrix placeholder. |
| `tests/test_bytes.py` | `TestBytesGetEncoding::test_get_encoding_utf8` | 72 |  |
| `tests/test_bytes.py` | `TestBytesGetEncoding::test_get_encoding_utf16_le` | 79 |  |
| `tests/test_bytes.py` | `TestBytesGetEncoding::test_get_encoding_latin1` | 55 | Valid narrow contract. Only type/presence assertion; behavioral regression coverage is weak. |
| `tests/test_bytes.py` | `TestBytesToString::test_to_string_utf8` | 79 |  |
| `tests/test_bytes.py` | `TestBytesToString::test_to_string_utf16_le` | 79 |  |
| `tests/test_bytes.py` | `TestBytesToString::test_to_string_unicode` | 82 |  |
| `tests/test_bytes.py` | `TestBytesToString::test_to_string_already_string` | 79 |  |
| `tests/test_bytes.py` | `TestBytesToString::test_to_string_special_chars` | 79 |  |
| `tests/test_bytes.py` | `TestBytesToString::test_to_string_emoji` | 72 |  |
| `tests/test_bytes.py` | `test_bytes_instance_helpers` | 72 |  |
| `tests/test_bytes.py` | `TestBytesInstance::test_bytes_instance_init_none` | 55 | Valid narrow contract. Narrow constructor/property state check. |
| `tests/test_bytes.py` | `TestBytesInstance::test_bytes_instance_init_with_data` | 55 | Narrow constructor/property state check. |
| `tests/test_bytes.py` | `TestBytesInstance::test_bytes_instance_get_encoding_forwarding` | 72 |  |
| `tests/test_bytes.py` | `TestBytesInstance::test_bytes_instance_to_string_forwarding` | 79 |  |
| `tests/test_bytes.py` | `TestBytesInstance::test_bytes_instance_get_encoding_utf16_forwarding` | 79 |  |
| `tests/test_bytes.py` | `TestBytesInstance::test_bytes_instance_to_string_unicode_forwarding` | 82 |  |
| `tests/test_bytes.py` | `TestBytesInstance::test_bytes_instance_getattribute_non_forwarded` | 82 |  |
| `tests/test_bytes.py` | `TestBytesInstance::test_bytes_instance_chained_operations` | 79 |  |
| `tests/test_bytes.py` | `TestBytesInstance::test_bytes_instance_special_chars` | 72 |  |
| `tests/test_bytes_integration.py` | — | 1 | No test functions; required matrix placeholder. |
| `tests/test_bytes_integration_negative.py` | — | 1 | No test functions; required matrix placeholder. |
| `tests/test_bytes_negative.py` | `TestBytesGetEncoding::test_get_encoding_empty` | 75 | Distinct canonical regression case. |
| `tests/test_bytes_negative.py` | `TestBytesNegative::test_get_encoding_invalid_bytes` | 55 | Valid narrow contract. Only type/presence assertion; behavioral regression coverage is weak. |
| `tests/test_bytes_negative.py` | `TestBytesNegative::test_to_string_mixed_encodings` | 72 | Distinct canonical regression case. |
| `tests/test_bytes_negative.py` | `TestBytesInstance::test_bytes_instance_ensure_raises` | 70 | Exercises private implementation detail; refactor-sensitive. |
| `tests/test_bytes_negative.py` | `TestBytesInstance::test_bytes_instance_none_data_raises_on_forward` | 81 | Distinct canonical regression case. |
| `tests/test_bytes_negative.py` | `TestBytesInstance::test_bytes_instance_empty_data` | 75 | Distinct canonical regression case. |
| `tests/test_cache.py` | `test_cache_basic` | 82 |  |
| `tests/test_cache.py` | `test_cache_with_args` | 79 |  |
| `tests/test_cache.py` | `test_cache_with_kwargs` | 79 |  |
| `tests/test_cache.py` | `test_cached_function_basic` | 79 |  |
| `tests/test_cache.py` | `test_cached_function_different_args` | 79 |  |
| `tests/test_cache.py` | `test_cached_function_kwargs` | 79 |  |
| `tests/test_cache.py` | `test_cache_update_counter` | 79 |  |
| `tests/test_cache.py` | `test_cache_without_bench_parameter` | 82 |  |
| `tests/test_cache.py` | `test_cache_value_alias` | 73 |  |
| `tests/test_cache.py` | `test_cached_function_value` | 73 |  |
| `tests/test_cache.py` | `TestCacheEdgeCases::test_cache_run_updates_stored_output` | 79 |  |
| `tests/test_cache.py` | `TestCacheEdgeCases::test_cache_run_calls_bench_end` | 66 | Mock-heavy interaction check; limited real implementation coverage. |
| `tests/test_cache.py` | `TestCacheEdgeCases::test_cached_function_cache_flush` | 82 |  |
| `tests/test_cache.py` | `TestCacheEdgeCases::test_cached_function_multiple_args_creates_separate_caches` | 79 |  |
| `tests/test_cache.py` | `TestCacheEdgeCases::test_cached_function_kwargs_creates_separate_cache` | 82 |  |
| `tests/test_cache.py` | `TestCacheEdgeCases::test_cached_function_return_value_recursion` | 79 |  |
| `tests/test_cache.py` | `TestCacheEdgeCases::test_cached_function_counter_increments` | 79 |  |
| `tests/test_cache.py` | `TestCacheEdgeCases::test_cache_lock_usage` | 55 | Valid narrow contract. Only type/presence assertion; behavioral regression coverage is weak. |
| `tests/test_cache.py` | `TestCacheEdgeCases::test_cached_function_lock_usage` | 55 | Valid narrow contract. Only type/presence assertion; behavioral regression coverage is weak. |
| `tests/test_cache.py` | `TestCacheEdgeCases::test_cache_with_complex_kwargs` | 79 |  |
| `tests/test_cache.py` | `TestCacheEdgeCases::test_cached_function_with_no_args` | 82 |  |
| `tests/test_cache_integration.py` | — | 1 | No test functions; required matrix placeholder. |
| `tests/test_cache_integration_negative.py` | — | 1 | No test functions; required matrix placeholder. |
| `tests/test_cache_negative.py` | `test_cache_update_every_zero` | 79 | Distinct canonical regression case. |
| `tests/test_cache_negative.py` | `test_cache_with_exception_in_func` | 78 | Distinct canonical regression case. |
| `tests/test_cache_negative.py` | `test_cached_function_with_mutable_args` | 79 | Distinct canonical regression case. |
| `tests/test_cache_negative.py` | `test_cache_attribute_error_recovery` | 85 | Distinct canonical regression case. |
| `tests/test_cli.py` | `test_cli_import` | 50 | Valid public-export smoke test; weak behavioral signal. |
| `tests/test_cli.py` | `test_cli_callable` | 66 |  |
| `tests/test_cli.py` | `test_cli_get_y_n_default` | 66 |  |
| `tests/test_cli.py` | `test_cli_get_int` | 73 |  |
| `tests/test_cli.py` | `test_cli_get_ints` | 73 |  |
| `tests/test_cli.py` | `test_cli_wait_update` | 72 |  |
| `tests/test_cli.py` | `test_cli_progressbar` | 72 |  |
| `tests/test_cli.py` | `test_cli_progressbar_reverse_and_overflow` | 55 | Valid narrow contract. Only type/presence assertion; behavioral regression coverage is weak. |
| `tests/test_cli.py` | `TestCLIWaitUpdate::test_wait_update_position_0` | 79 |  |
| `tests/test_cli.py` | `TestCLIWaitUpdate::test_wait_update_position_1` | 79 |  |
| `tests/test_cli.py` | `TestCLIWaitUpdate::test_wait_update_position_2` | 79 |  |
| `tests/test_cli.py` | `TestCLIWaitUpdate::test_wait_update_position_3` | 79 |  |
| `tests/test_cli.py` | `TestCLIWaitUpdate::test_wait_update_verbose_true` | 73 | Mock-heavy interaction check; limited real implementation coverage. |
| `tests/test_cli.py` | `TestCLIWaitUpdate::test_wait_update_full_cycle` | 79 |  |
| `tests/test_cli.py` | `TestCLIGetIntegerAliases::test_get_integer_alias` | 73 |  |
| `tests/test_cli.py` | `TestCLIGetIntegerAliases::test_get_integers_alias` | 73 |  |
| `tests/test_cli.py` | `TestCLIGetDate::test_get_date_empty_input_no_always_return` | 60 | Valid exact-value or state-transition contract. |
| `tests/test_cli.py` | `TestCLIProgressbarEdgeCases::test_progressbar_reverse_overflow` | 55 | Valid narrow contract. Only type/presence assertion; behavioral regression coverage is weak. |
| `tests/test_cli.py` | `TestCLIProgressbarEdgeCases::test_progressbar_zero_total` | 55 | Valid narrow contract. Only type/presence assertion; behavioral regression coverage is weak. |
| `tests/test_cli.py` | `TestCLIGetIntsEdgeCases::test_get_ints_multiline_input` | 73 |  |
| `tests/test_cli.py` | `TestCLIGetIntsEdgeCases::test_get_ints_with_spaces` | 73 |  |
| `tests/test_cli.py` | `test_cli_get_y_n_get_key_returns_none_uses_default` | 64 | Exercises private implementation detail; refactor-sensitive. |
| `tests/test_cli.py` | `test_cli_get_y_n_translate_mismatch_prints` | 61 | Exercises private implementation detail; refactor-sensitive. |
| `tests/test_cli.py` | `test_cli_progressbar_windows_branch` | 55 | Valid narrow contract. Only type/presence assertion; behavioral regression coverage is weak. |
| `tests/test_cli.py` | `test_cli_multiline_input` | 73 |  |
| `tests/test_cli.py` | `test_cli_get_date_optional` | 60 | Valid exact-value or state-transition contract. |
| `tests/test_cli.py` | `test_cli_get_date_retry_and_success` | 68 | Wall-clock dependence adds timing-flake risk. |
| `tests/test_cli_integration.py` | — | 1 | No test functions; required matrix placeholder. |
| `tests/test_cli_integration_negative.py` | — | 1 | No test functions; required matrix placeholder. |
| `tests/test_cli_negative.py` | `test_cli_get_y_n_invalid_no_default` | 75 |  |
| `tests/test_cli_negative.py` | `test_cli_get_y_n_invalid` | 69 | Distinct canonical regression case. |
| `tests/test_cli_negative.py` | `test_cli_get_ints_invalid` | 75 | Distinct canonical regression case. |
| `tests/test_cli_negative.py` | `TestCLIGetDate::test_get_date_invalid_day` | 73 | Re-scored after removing shadowing/stale-suite interference. |
| `tests/test_cli_negative.py` | `TestCLIGetDate::test_get_date_invalid_month` | 73 | Re-scored after removing shadowing/stale-suite interference. |
| `tests/test_cli_negative.py` | `TestCLIGetDate::test_get_date_invalid_year` | 73 | Re-scored after removing shadowing/stale-suite interference. |
| `tests/test_cli_negative.py` | `TestCLIGetDate::test_get_date_always_return_empty_input` | 73 | Re-scored after removing shadowing/stale-suite interference. |
| `tests/test_cli_negative.py` | `test_cli_get_y_n_ctrl_c_raises_keyboard_interrupt` | 67 | Exercises private implementation detail; refactor-sensitive. |
| `tests/test_console.py` | `test_console_width` | 79 |  |
| `tests/test_console.py` | `test_console_height` | 79 | Skipped in current environment; platform/dependency branch not runtime-verified here. |
| `tests/test_console.py` | `test_console_width_always_positive` | 79 |  |
| `tests/test_console.py` | `test_console_width_reasonable` | 79 |  |
| `tests/test_console.py` | `TestConsoleCoverage::test_fit_basic` | 72 |  |
| `tests/test_console.py` | `TestConsoleCoverage::test_fit_with_sep` | 79 |  |
| `tests/test_console.py` | `TestConsoleCoverage::test_fit_reverse` | 72 |  |
| `tests/test_console.py` | `TestConsoleCoverage::test_fit_long_string_needs_cutting` | 79 |  |
| `tests/test_console.py` | `TestConsoleCoverage::test_fit_strings_already_fit` | 79 |  |
| `tests/test_console.py` | `TestConsoleCoverage::test_fit_with_double_width_chars` | 55 | Valid narrow contract. Only type/presence assertion; behavioral regression coverage is weak. |
| `tests/test_console.py` | `TestConsoleCoverage::test_fit_windows_width_adjustment` | 55 | Valid narrow contract. Only type/presence assertion; behavioral regression coverage is weak. |
| `tests/test_console.py` | `TestConsoleCoverage::test_fit_finding_longest_string` | 72 |  |
| `tests/test_console.py` | `TestConsoleCoverage::test_fit_adjusting_spaces` | 55 | Valid narrow contract. Only type/presence assertion; behavioral regression coverage is weak. |
| `tests/test_console.py` | `test_console_blink_interrupt` | 73 | Re-scored after removing shadowing/stale-suite interference. |
| `tests/test_console.py` | `test_console_blink_windows_mode_call` | 61 | Wall-clock dependence adds timing-flake risk. |
| `tests/test_console.py` | `TestConsoleBlink::test_blink_width_none` | 75 |  |
| `tests/test_console.py` | `TestConsoleBlink::test_blink_height_none` | 75 |  |
| `tests/test_console.py` | `TestConsoleGetOutputChardet::test_get_output_chardet_fallback` | 61 | Mock-heavy interaction check; limited real implementation coverage. Exercises private implementation detail; refactor-sensitive. |
| `tests/test_console.py` | `TestConsoleGetOutputPrintStd::test_get_output_print_std_true` | 61 | Mock-heavy interaction check; limited real implementation coverage. Exercises private implementation detail; refactor-sensitive. |
| `tests/test_console.py` | `TestConsoleGetOutputEmptyHook::test_get_output_no_hooks` | 55 | Valid narrow contract. Only type/presence assertion; behavioral regression coverage is weak. |
| `tests/test_console.py` | `TestConsoleGetOutputCreateCmdSubprocess::test_get_output_create_cmd_subprocess` | 66 | Mock-heavy interaction check; limited real implementation coverage. Skipped in current environment; platform/dependency branch not runtime-verified here. |
| `tests/test_console.py` | `TestConsoleFitPadding::test_fit_padding_needed` | 79 |  |
| `tests/test_console.py` | `TestConsoleFitPadding::test_fit_exact_length` | 55 | Valid narrow contract. Only type/presence assertion; behavioral regression coverage is weak. |
| `tests/test_console.py` | `TestConsoleFitPadding::test_fit_too_long` | 55 | Valid narrow contract. Only type/presence assertion; behavioral regression coverage is weak. |
| `tests/test_console.py` | `TestConsoleWindowsCodepage::test_get_output_windows_cp65001` | 55 | Valid narrow contract. Skipped in current environment; platform/dependency branch not runtime-verified here. |
| `tests/test_console.py` | `TestConsoleWindowsCodepage::test_get_output_windows_cp866_fallback` | 55 | Valid narrow contract. Skipped in current environment; platform/dependency branch not runtime-verified here. |
| `tests/test_console.py` | `test_console_watch_callable_renders_and_quits` | 76 | Re-scored after removing shadowing/stale-suite interference. |
| `tests/test_console.py` | `test_console_watch_command_combines_streams` | 76 | Re-scored after removing shadowing/stale-suite interference. |
| `tests/test_console.py` | `test_console_get_output_empty_commands` | 78 | Re-scored after removing shadowing/stale-suite interference. |
| `tests/test_console.py` | `test_console_fit_reverse_prefix_length` | 55 | Valid narrow contract. Only type/presence assertion; behavioral regression coverage is weak. |
| `tests/test_console.py` | `test_console_run_uses_stored_defaults` | 76 |  |
| `tests/test_console.py` | `test_console_get_output_windows_fallback_decoding` | 73 |  |
| `tests/test_console.py` | `test_console_get_output_unknown_os_sets_universal` | 66 |  |
| `tests/test_console.py` | `test_console__get_output_decoding_and_print` | 70 | Exercises private implementation detail; refactor-sensitive. |
| `tests/test_console.py` | `test_console_get_output_injects_py_unbuffered` | 73 |  |
| `tests/test_console.py` | `test_console_get_output_timeout_flag` | 76 | Mock-heavy interaction check; limited real implementation coverage. |
| `tests/test_console.py` | `test_console_get_output_windows_cp65001_cached` | 73 |  |
| `tests/test_console.py` | `test_console_get_output_windows_cp65001_failed_cached` | 73 |  |
| `tests/test_console.py` | `test_console_get_output_windows_detects_cp65001` | 73 |  |
| `tests/test_console.py` | `test_console_get_output_create_cmd_subprocess_builds_cmd` | 76 |  |
| `tests/test_console.py` | `test_console_fit_wide_char_padding_branch` | 66 |  |
| `tests/test_console.py` | `test_console_height_windows` | 73 |  |
| `tests/test_console.py` | `test_console_height_unix` | 73 |  |
| `tests/test_console.py` | `test_console_get_output_threads_and_hooks` | 64 | Exercises private implementation detail; refactor-sensitive. |
| `tests/test_console.py` | `test_console_timeout_kills_process` | 66 | Exercises private implementation detail; refactor-sensitive. |
| `tests/test_console.py` | `test_console_timeout_return_tuple_when_timeout` | 66 |  |
| `tests/test_console_integration.py` | `TestConsoleCoverage::test_get_output_basic` | 67 | Exercises private implementation detail; refactor-sensitive. |
| `tests/test_console_integration.py` | `TestConsoleCoverage::test_get_output_pure_shell` | 72 | Distinct canonical regression case. |
| `tests/test_console_integration.py` | `TestConsoleCoverage::test_get_output_string_command` | 72 | Distinct canonical regression case. |
| `tests/test_console_integration.py` | `TestConsoleCoverage::test_get_output_list_commands` | 67 | Exercises private implementation detail; refactor-sensitive. |
| `tests/test_console_integration.py` | `TestConsoleCoverage::test_get_output_hooks` | 67 | Exercises private implementation detail; refactor-sensitive. |
| `tests/test_console_integration.py` | `TestConsoleCoverage::test_get_output_return_merged_false` | 70 | Exercises private implementation detail; refactor-sensitive. |
| `tests/test_console_integration.py` | `TestConsoleCoverage::test_get_output_with_timeout` | 67 | Exercises private implementation detail; refactor-sensitive. |
| `tests/test_console_integration.py` | `TestConsoleCoverage::test_get_output_python_auto_disable_buffering` | 55 | Valid narrow contract. Only type/presence assertion; behavioral regression coverage is weak. |
| `tests/test_console_integration.py` | `TestConsoleCoverage::test_get_output_python_with_print_std` | 72 | Distinct canonical regression case. |
| `tests/test_console_integration.py` | `TestConsoleCoverage::test_get_output_python_already_has_u_flag` | 72 | Distinct canonical regression case. |
| `tests/test_console_integration.py` | `TestConsoleCoverage::test_get_output_py_command` | 55 | Valid narrow contract. Skipped in current environment; platform/dependency branch not runtime-verified here. |
| `tests/test_console_integration.py` | `TestConsoleCoverage::test_get_output_create_cmd_subprocess` | 72 | Skipped in current environment; platform/dependency branch not runtime-verified here. |
| `tests/test_console_integration.py` | `TestConsoleCoverage::test_get_output_manual_decoding` | 67 | Exercises private implementation detail; refactor-sensitive. |
| `tests/test_console_integration.py` | `TestConsoleCoverage::test_height_unix` | 73 | Skipped in current environment; platform/dependency branch not runtime-verified here. |
| `tests/test_console_integration.py` | `TestConsoleCoverage::test_get_output_with_decoding_fallback` | 67 | Exercises private implementation detail; refactor-sensitive. |
| `tests/test_console_integration.py` | `TestConsoleCoverage::test_get_output_print_std_colored_output` | 67 | Exercises private implementation detail; refactor-sensitive. |
| `tests/test_console_integration.py` | `TestConsoleCoverage::test_get_output_threading_execution` | 72 | Distinct canonical regression case. |
| `tests/test_console_integration.py` | `test_console_clean_branches` | 73 | Re-scored after removing shadowing/stale-suite interference. |
| `tests/test_console_integration.py` | `test_console_get_output_print_std_bytes` | 76 | Mock-heavy interaction check; limited real implementation coverage. |
| `tests/test_console_integration.py` | `test_console_get_output_return_merged_bytes` | 79 |  |
| `tests/test_console_integration_negative.py` | `TestConsoleCoverage::test_get_output_file_not_found_debug` | 78 | Distinct canonical regression case. |
| `tests/test_console_integration_negative.py` | `TestConsoleCoverage::test_get_output_timeout_reached` | 72 | Distinct canonical regression case. |
| `tests/test_console_negative.py` | `TestConsoleCoverage::test_get_output_empty_commands` | 81 | Distinct canonical regression case. |
| `tests/test_console_negative.py` | `TestConsoleCoverage::test_get_output_decoding_universal_newlines_conflict` | 70 | Exercises private implementation detail; refactor-sensitive. |
| `tests/test_console_negative.py` | `test_console_get_output_decoding_conflict` | 78 | Distinct canonical regression case. |
| `tests/test_console_negative.py` | `test_console_get_output_invalid_decoding_combo` | 75 | Distinct canonical regression case. |
| `tests/test_console_negative.py` | `test_console_fit_returns_empty_when_width_non_positive` | 82 | Distinct canonical regression case. |
| `tests/test_console_negative.py` | `test_console_height_no_stty` | 72 | Distinct canonical regression case. |
| `tests/test_console_negative.py` | `test_console__resolve_commands_raises` | 78 | Distinct canonical regression case. |
| `tests/test_console_negative.py` | `test_console_get_output_invalid_decoding_and_universal` | 75 | Distinct canonical regression case. |
| `tests/test_console_negative.py` | `test_console_get_output_empty` | 63 | Exact duplicate of `tests/test_console.py::test_console_get_output_empty_commands`; redundant regression signal. |
| `tests/test_console_negative.py` | `test_console_watch_rejects_nonpositive_timing` | 78 | Re-scored after removing shadowing/stale-suite interference. |
| `tests/test_const.py` | `test_newline` | 60 | Valid exact-value or state-transition contract. |
| `tests/test_const.py` | `test_ruble` | 79 |  |
| `tests/test_const.py` | `test_backslash` | 60 | Valid exact-value or state-transition contract. |
| `tests/test_const.py` | `test_newline2` | 60 | Valid exact-value or state-transition contract. |
| `tests/test_const.py` | `test_rtl` | 60 | Valid exact-value or state-transition contract. |
| `tests/test_const.py` | `test_kib` | 60 | Valid exact-value or state-transition contract. |
| `tests/test_const.py` | `test_mib` | 79 |  |
| `tests/test_const.py` | `test_gib` | 79 |  |
| `tests/test_const.py` | `test_tib` | 79 |  |
| `tests/test_const.py` | `test_constants_are_immutable_types` | 55 | Valid narrow contract. Only type/presence assertion; behavioral regression coverage is weak. |
| `tests/test_const.py` | `test_byte_size_relationships` | 82 |  |
| `tests/test_const_integration.py` | — | 1 | No test functions; required matrix placeholder. |
| `tests/test_const_integration_negative.py` | — | 1 | No test functions; required matrix placeholder. |
| `tests/test_const_negative.py` | — | 1 | No test functions; required matrix placeholder. |
| `tests/test_dict.py` | `TestImDict::test_imdict_creation` | 79 |  |
| `tests/test_dict.py` | `TestImDict::test_imdict_hashable` | 55 | Valid narrow contract. Only type/presence assertion; behavioral regression coverage is weak. |
| `tests/test_dict.py` | `TestDictIterable::test_iterable_basic` | 72 |  |
| `tests/test_dict.py` | `TestDictIterable::test_iterable_copy` | 79 |  |
| `tests/test_dict.py` | `TestDictSortedByKey::test_sorted_by_key_basic` | 79 |  |
| `tests/test_dict.py` | `TestDictSortedByKey::test_sorted_by_key_case_insensitive` | 72 |  |
| `tests/test_dict.py` | `TestDictSortedByKey::test_sorted_by_key_returns_ordered_dict` | 55 | Valid narrow contract. Only type/presence assertion; behavioral regression coverage is weak. |
| `tests/test_dict.py` | `TestDictSortedByKey::test_sorted_by_key_custom_func` | 79 |  |
| `tests/test_dict.py` | `TestDictFromStr::test_from_str_basic` | 79 |  |
| `tests/test_dict.py` | `TestDictFromStr::test_from_str_empty` | 82 |  |
| `tests/test_dict.py` | `TestDictFromStr::test_from_str_nested` | 79 |  |
| `tests/test_dict.py` | `TestDictInstanceOf::test_isinstance_keys_true` | 72 |  |
| `tests/test_dict.py` | `TestDictInstanceOf::test_isinstance_keys_false` | 72 |  |
| `tests/test_dict.py` | `TestDictInstanceOf::test_isinstance_keys_multiple_types` | 72 |  |
| `tests/test_dict.py` | `TestDictInstanceOf::test_isinstance_values_true` | 72 |  |
| `tests/test_dict.py` | `TestDictInstanceOf::test_isinstance_values_false` | 72 |  |
| `tests/test_dict.py` | `TestDictInstanceOf::test_isinstance_values_multiple_types` | 72 |  |
| `tests/test_dict.py` | `TestDictLambdaMethods::test_all_keys_lambda_basic` | 79 |  |
| `tests/test_dict.py` | `TestDictLambdaMethods::test_all_keys_lambda_with_args` | 79 |  |
| `tests/test_dict.py` | `TestDictLambdaMethods::test_all_values_lambda_basic` | 79 |  |
| `tests/test_dict.py` | `TestDictLambdaMethods::test_all_values_lambda_with_args` | 79 |  |
| `tests/test_dict.py` | `TestDictLambdaMethods::test_all_values_lambda_str_conversion` | 79 |  |
| `tests/test_dict.py` | `TestDictHelpers::test_str_lower_of_dict_key` | 79 |  |
| `tests/test_dict.py` | `TestDictHelpers::test_get_dict_key` | 79 |  |
| `tests/test_dict.py` | `TestDictNegative::test_imdict_empty` | 82 |  |
| `tests/test_dict.py` | `TestDictNegative::test_imdict_nested_mutable` | 79 |  |
| `tests/test_dict.py` | `TestDictNegative::test_iterable_empty_dict` | 82 |  |
| `tests/test_dict.py` | `TestDictNegative::test_sorted_by_key_empty` | 82 |  |
| `tests/test_dict.py` | `TestDictNegative::test_from_str_null` | 79 |  |
| `tests/test_dict.py` | `TestDictNegative::test_isinstance_keys_empty_dict` | 75 |  |
| `tests/test_dict.py` | `TestDictNegative::test_isinstance_values_empty_dict` | 75 |  |
| `tests/test_dict.py` | `TestDictNegative::test_all_keys_lambda_empty` | 82 |  |
| `tests/test_dict.py` | `TestDictNegative::test_all_values_lambda_empty` | 82 |  |
| `tests/test_dict.py` | `test_dict_instance_helpers` | 82 |  |
| `tests/test_dict.py` | `TestDictInstance::test_dict_instance_init_none` | 55 | Narrow constructor/property state check. |
| `tests/test_dict.py` | `TestDictInstance::test_dict_instance_init_with_data` | 55 | Narrow constructor/property state check. |
| `tests/test_dict.py` | `TestDictInstance::test_dict_instance_iterable_forwarding` | 72 |  |
| `tests/test_dict.py` | `TestDictInstance::test_dict_instance_isinstance_keys_forwarding` | 72 |  |
| `tests/test_dict.py` | `TestDictInstance::test_dict_instance_isinstance_values_forwarding` | 72 |  |
| `tests/test_dict.py` | `TestDictInstance::test_dict_instance_all_keys_lambda_forwarding` | 79 |  |
| `tests/test_dict.py` | `TestDictInstance::test_dict_instance_all_values_lambda_forwarding` | 79 |  |
| `tests/test_dict.py` | `TestDictInstance::test_dict_instance_sorted_by_key_forwarding` | 79 |  |
| `tests/test_dict.py` | `TestDictInstance::test_dict_instance_lambda_with_kwargs` | 79 |  |
| `tests/test_dict.py` | `TestDictInstance::test_dict_instance_getattribute_non_forwarded` | 82 |  |
| `tests/test_dict_integration.py` | — | 1 | No test functions; required matrix placeholder. |
| `tests/test_dict_integration_negative.py` | — | 1 | No test functions; required matrix placeholder. |
| `tests/test_dict_negative.py` | `TestImDict::test_imdict_setitem_raises` | 78 | Distinct canonical regression case. |
| `tests/test_dict_negative.py` | `TestImDict::test_imdict_delitem_raises` | 78 | Distinct canonical regression case. |
| `tests/test_dict_negative.py` | `TestImDict::test_imdict_clear_raises` | 78 | Distinct canonical regression case. |
| `tests/test_dict_negative.py` | `TestImDict::test_imdict_update_raises` | 78 | Distinct canonical regression case. |
| `tests/test_dict_negative.py` | `TestImDict::test_imdict_pop_raises` | 78 | Distinct canonical regression case. |
| `tests/test_dict_negative.py` | `TestImDict::test_imdict_popitem_raises` | 78 | Distinct canonical regression case. |
| `tests/test_dict_negative.py` | `TestImDict::test_imdict_setdefault_raises` | 78 | Distinct canonical regression case. |
| `tests/test_dict_negative.py` | `TestDictIterable::test_iterable_invalid_type` | 81 | Distinct canonical regression case. |
| `tests/test_dict_negative.py` | `TestDictFromStr::test_from_str_invalid` | 55 | Uses broad `pytest.raises(Exception)`; may pass for wrong failure reason. |
| `tests/test_dict_negative.py` | `TestDictFromStr::test_from_str_list_raises` | 78 | Distinct canonical regression case. |
| `tests/test_dict_negative.py` | `TestDictNegative::test_sorted_by_key_invalid_func` | 55 | Uses broad `pytest.raises(Exception)`; may pass for wrong failure reason. |
| `tests/test_dict_negative.py` | `TestDictNegative::test_from_str_malformed` | 55 | Uses broad `pytest.raises(Exception)`; may pass for wrong failure reason. |
| `tests/test_dict_negative.py` | `TestDictNegative::test_all_keys_lambda_exception` | 55 | Uses broad `pytest.raises(Exception)`; may pass for wrong failure reason. |
| `tests/test_dict_negative.py` | `TestDictNegative::test_all_values_lambda_exception` | 55 | Uses broad `pytest.raises(Exception)`; may pass for wrong failure reason. |
| `tests/test_dict_negative.py` | `TestDictInstance::test_dict_instance_ensure_raises` | 70 | Exercises private implementation detail; refactor-sensitive. |
| `tests/test_dict_negative.py` | `TestDictInstance::test_dict_instance_none_data_raises_on_forward` | 81 | Distinct canonical regression case. |
| `tests/test_dir.py` | `TestDirInstanceComprehensive::test_instance_string_property` | 55 | Narrow constructor/property state check. |
| `tests/test_dir.py` | `TestDirDeletePermissionHandling::test_delete_permission_error_with_skip` | 75 |  |
| `tests/test_dir.py` | `TestDirDeletePermissionHandling::test_delete_permission_error_skip_quiet` | 69 | Mock-heavy interaction check; limited real implementation coverage. |
| `tests/test_dir.py` | `TestDirDeletePermissionHandling::test_delete_without_remove_readonly` | 66 | Mock-heavy interaction check; limited real implementation coverage. |
| `tests/test_dir.py` | `TestDirDeletePermissionHandling::test_delete_without_readonly_with_skip_permission` | 69 | Mock-heavy interaction check; limited real implementation coverage. |
| `tests/test_dir.py` | `TestDirCopySymlinksAndErrors::test_copy_permission_error_with_skip` | 69 | Mock-heavy interaction check; limited real implementation coverage. |
| `tests/test_dir.py` | `TestDirCopySymlinksAndErrors::test_copy_file_not_found_error` | 69 | Mock-heavy interaction check; limited real implementation coverage. |
| `tests/test_dir.py` | `TestDirCopySymlinksAndErrors::test_copy_os_error` | 69 | Mock-heavy interaction check; limited real implementation coverage. |
| `tests/test_dir_integration.py` | `test_dir_create` | 77 | Distinct canonical regression case. |
| `tests/test_dir_integration.py` | `test_dir_create_nested` | 77 | Distinct canonical regression case. |
| `tests/test_dir_integration.py` | `test_dir_create_existing` | 77 | Distinct canonical regression case. |
| `tests/test_dir_integration.py` | `test_dir_list_of_entries` | 77 | Distinct canonical regression case. |
| `tests/test_dir_integration.py` | `test_dir_list_of_files` | 80 | Distinct canonical regression case. |
| `tests/test_dir_integration.py` | `test_dir_list_of_dirs` | 80 | Distinct canonical regression case. |
| `tests/test_dir_integration.py` | `test_dir_number_of_files` | 84 | Distinct canonical regression case. |
| `tests/test_dir_integration.py` | `test_dir_exist` | 77 | Distinct canonical regression case. |
| `tests/test_dir_integration.py` | `test_dir_delete` | 77 | Distinct canonical regression case. |
| `tests/test_dir_integration.py` | `TestDirCoverage::test_number_of_files_verbose` | 87 | Distinct canonical regression case. |
| `tests/test_dir_integration.py` | `TestDirCoverage::test_batch_rename` | 80 | Distinct canonical regression case. |
| `tests/test_dir_integration.py` | `TestDirCoverage::test_batch_rename_quiet` | 77 | Distinct canonical regression case. |
| `tests/test_dir_integration.py` | `TestDirCoverage::test_cleanup` | 80 | Distinct canonical regression case. |
| `tests/test_dir_integration.py` | `TestDirCoverage::test_cleanup_with_quiet_permission_error` | 87 | Distinct canonical regression case. |
| `tests/test_dir_integration.py` | `TestDirCoverage::test_dir_instance_rename_and_delete` | 87 | Distinct canonical regression case. |
| `tests/test_dir_integration.py` | `TestDirCoverage::test_delete_cleanup_mode` | 80 | Distinct canonical regression case. |
| `tests/test_dir_integration.py` | `TestDirCoverage::test_copy_basic` | 80 | Distinct canonical regression case. |
| `tests/test_dir_integration.py` | `TestDirCoverage::test_copy_verbose` | 77 | Distinct canonical regression case. |
| `tests/test_dir_integration.py` | `TestDirCoverage::test_copy_with_ignore` | 77 | Distinct canonical regression case. |
| `tests/test_dir_integration.py` | `TestDirCoverage::test_move` | 80 | Distinct canonical regression case. |
| `tests/test_dir_integration.py` | `TestDirCoverage::test_move_verbose` | 84 | Distinct canonical regression case. |
| `tests/test_dir_integration.py` | `TestDirCoverage::test_move_with_quiet_permission_error` | 80 | Distinct canonical regression case. |
| `tests/test_dir_integration.py` | `TestDirCoverage::test_exists_alias` | 77 | Distinct canonical regression case. |
| `tests/test_dir_integration.py` | `TestDirCoverage::test_get_size` | 84 | Distinct canonical regression case. |
| `tests/test_dir_integration.py` | `TestDirCoverage::test_get_modification_time` | 84 | Distinct canonical regression case. |
| `tests/test_dir_integration.py` | `TestDirCoverage::test_get_free_space` | 84 | Distinct canonical regression case. |
| `tests/test_dir_integration.py` | `TestDirInstanceComprehensive::test_instance_create` | 77 | Distinct canonical regression case. |
| `tests/test_dir_integration.py` | `TestDirInstanceComprehensive::test_instance_move` | 84 | Distinct canonical regression case. |
| `tests/test_dir_integration.py` | `TestDirInstanceComprehensive::test_instance_delete` | 77 | Distinct canonical regression case. |
| `tests/test_dir_integration.py` | `TestDirInstanceComprehensive::test_instance_delete_with_cleanup` | 84 | Distinct canonical regression case. |
| `tests/test_dir_integration.py` | `TestDirInstanceComprehensive::test_instance_delete_with_skip_permission_error` | 80 | Distinct canonical regression case. |
| `tests/test_dir_integration.py` | `TestDirInstanceComprehensive::test_instance_delete_with_quiet_permission_error` | 80 | Distinct canonical regression case. |
| `tests/test_dir_integration.py` | `TestDirCopySymlinksAndErrors::test_copy_with_symlinks` | 77 | Distinct canonical regression case. |
| `tests/test_dir_integration.py` | `test_dir_instance_move_updates_path` | 87 | Distinct canonical regression case. |
| `tests/test_dir_integration.py` | `test_dir_number_of_files_and_get_size` | 84 | Distinct canonical regression case. |
| `tests/test_dir_integration.py` | `test_dir_batch_rename` | 77 | Distinct canonical regression case. |
| `tests/test_dir_integration.py` | `test_dir_copy_with_ignore_and_errors` | 74 | Distinct canonical regression case. |
| `tests/test_dir_integration.py` | `test_dir_exist_alias` | 77 | Distinct canonical regression case. |
| `tests/test_dir_integration_negative.py` | `test_dir_list_of_entries_nonexistent` | 81 | Distinct canonical regression case. |
| `tests/test_dir_integration_negative.py` | `test_dir_list_of_files_nonexistent` | 81 | Distinct canonical regression case. |
| `tests/test_dir_integration_negative.py` | `test_dir_list_of_dirs_nonexistent` | 81 | Distinct canonical regression case. |
| `tests/test_dir_integration_negative.py` | `test_dir_number_of_files_nonexistent` | 81 | Distinct canonical regression case. |
| `tests/test_dir_integration_negative.py` | `TestDirCoverage::test_get_size_nonexistent` | 81 | Distinct canonical regression case. |
| `tests/test_dir_integration_negative.py` | `test_dir_number_of_files_missing` | 86 | Distinct canonical regression case. |
| `tests/test_dir_integration_negative.py` | `test_dir_delete_skip_permission` | 80 | Distinct canonical regression case. |
| `tests/test_dir_negative.py` | `TestDirMissingCoverage::test_copy_symlink_with_existing_destination` | 77 | Distinct canonical regression case. |
| `tests/test_dir_negative.py` | `TestDirMissingCoverage::test_copy_file_not_found_error_raises` | 80 | Distinct canonical regression case. |
| `tests/test_dir_negative.py` | `TestDirCopySymlinksAndErrors::test_copy_permission_error_no_skip` | 75 | Distinct canonical regression case. |
| `tests/test_dir_negative.py` | `TestDirCopySymlinksAndErrors::test_copy_os_error_no_skip` | 75 | Distinct canonical regression case. |
| `tests/test_dir_negative.py` | `TestDirNegativeCases::test_instance_create_no_path` | 78 | Distinct canonical regression case. |
| `tests/test_dir_negative.py` | `TestDirNegativeCases::test_instance_rename_no_path` | 78 | Distinct canonical regression case. |
| `tests/test_dir_negative.py` | `TestDirNegativeCases::test_instance_move_no_path` | 78 | Distinct canonical regression case. |
| `tests/test_dir_negative.py` | `TestDirNegativeCases::test_instance_delete_no_path` | 78 | Distinct canonical regression case. |
| `tests/test_dir_negative.py` | `test_dir_ensure_path_required` | 70 | Exercises private implementation detail; refactor-sensitive. |
| `tests/test_ffmpeg.py` | `test_ffmpeg_import` | 50 | Valid public-export smoke test; weak behavioral signal. |
| `tests/test_ffmpeg.py` | `test_ffmpeg_class_add_subtitles` | 76 |  |
| `tests/test_ffmpeg.py` | `test_ffmpeg_class_add_audio` | 73 |  |
| `tests/test_ffmpeg.py` | `test_ffmpeg_convert_avi_to_mkv` | 66 | Mock-heavy interaction check; limited real implementation coverage. |
| `tests/test_ffmpeg.py` | `test_ffmpeg_convert_to_mkv` | 66 | Mock-heavy interaction check; limited real implementation coverage. |
| `tests/test_ffmpeg.py` | `TestFFmpegCoverage::test_subtitles_instance_method` | 76 | Mock-heavy interaction check; limited real implementation coverage. |
| `tests/test_ffmpeg.py` | `TestFFmpegCoverage::test_audio_instance_method` | 76 | Mock-heavy interaction check; limited real implementation coverage. |
| `tests/test_ffmpeg.py` | `TestFFmpegCoverage::test_convert_avi_to_mkv_verbose` | 69 |  |
| `tests/test_ffmpeg.py` | `TestFFmpegCoverage::test_convert_to_mkv_verbose` | 69 |  |
| `tests/test_ffmpeg.py` | `test_ffmpeg_add_something_builds_commands` | 76 |  |
| `tests/test_ffmpeg.py` | `test_ffmpeg_instance_shortcuts` | 76 | Mock-heavy interaction check; limited real implementation coverage. |
| `tests/test_ffmpeg_integration.py` | — | 1 | No test functions; required matrix placeholder. |
| `tests/test_ffmpeg_integration_negative.py` | — | 1 | No test functions; required matrix placeholder. |
| `tests/test_ffmpeg_negative.py` | `test_ffmpeg_instance_requires_input` | 78 | Distinct canonical regression case. |
| `tests/test_ffmpeg_negative.py` | `test_ffmpeg_instance_requires_output` | 78 | Distinct canonical regression case. |
| `tests/test_ffmpeg_negative.py` | `test_ffmpeg_instance_missing_input_output` | 81 | Distinct canonical regression case. |
| `tests/test_ffmpeg_negative.py` | `test_ffmpeg_input_output_validation` | 70 | Exercises private implementation detail; refactor-sensitive. |
| `tests/test_file.py` | `TestFileCoverage::test_create_verbose_true` | 77 |  |
| `tests/test_file.py` | `TestFileCoverage::test_create_invalid_verbose_type` | 86 |  |
| `tests/test_file.py` | `TestFileCoverage::test_delete_verbose_true` | 77 |  |
| `tests/test_file.py` | `TestFileCoverage::test_delete_nonexistent_verbose_true` | 80 |  |
| `tests/test_file.py` | `TestFileCoverage::test_delete_with_sleep_check` | 77 |  |
| `tests/test_file.py` | `TestFileCoverage::test_get_encoding` | 77 |  |
| `tests/test_file.py` | `TestFileCoverage::test_get_encoding_with_count` | 55 | Valid narrow contract. Only type/presence assertion; behavioral regression coverage is weak. |
| `tests/test_file.py` | `TestFileCoverage::test_read_with_auto_detect_encoding` | 84 |  |
| `tests/test_file.py` | `TestFileCoverage::test_read_with_specific_encoding` | 84 |  |
| `tests/test_file.py` | `TestFileCoverage::test_backup` | 80 |  |
| `tests/test_file.py` | `TestFileCoverage::test_backup_verbose_true` | 77 |  |
| `tests/test_file.py` | `TestFileCoverage::test_hide_unix` | 77 |  |
| `tests/test_file.py` | `TestFileCoverage::test_hide_verbose_true` | 77 |  |
| `tests/test_file.py` | `test_file_string_property_pathlike` | 72 | Re-scored after removing shadowing/stale-suite interference. |
| `tests/test_file.py` | `test_file_hide_windows` | 78 |  |
| `tests/test_file.py` | `test_file_read_by_line_lookup_error` | 81 |  |
| `tests/test_file.py` | `test_file_format_size_human_readable_boundaries` | 82 |  |
| `tests/test_file.py` | `test_file_mime_fallback` | 71 |  |
| `tests/test_file.py` | `test_file_string_property` | 72 | Re-scored after removing shadowing/stale-suite interference. |
| `tests/test_file.py` | `test_read_lookuperror_falls_back_to_tis620` | 81 |  |
| `tests/test_file.py` | `test_read_unicode_decode_error_uses_cp1251` | 74 |  |
| `tests/test_file.py` | `test_format_size_handles_tib_boundary` | 72 |  |
| `tests/test_file.py` | `test_get_mime_windows_fallback` | 78 | Mock-heavy interaction check; limited real implementation coverage. |
| `tests/test_file_integration.py` | `test_file_create` | 77 | Distinct canonical regression case. |
| `tests/test_file_integration.py` | `test_file_create_with_subdirs` | 77 | Distinct canonical regression case. |
| `tests/test_file_integration.py` | `test_file_delete` | 77 | Distinct canonical regression case. |
| `tests/test_file_integration.py` | `test_file_copy` | 84 | Distinct canonical regression case. |
| `tests/test_file_integration.py` | `test_file_move` | 77 | Distinct canonical regression case. |
| `tests/test_file_integration.py` | `test_file_rename` | 77 | Distinct canonical regression case. |
| `tests/test_file_integration.py` | `test_file_wipe` | 84 | Distinct canonical regression case. |
| `tests/test_file_integration.py` | `test_file_exist` | 77 | Distinct canonical regression case. |
| `tests/test_file_integration.py` | `test_file_read` | 84 | Distinct canonical regression case. |
| `tests/test_file_integration.py` | `test_file_write` | 84 | Distinct canonical regression case. |
| `tests/test_file_integration.py` | `test_file_read_by_chunk_and_line` | 82 | Re-scored after removing shadowing/stale-suite interference. |
| `tests/test_file_integration.py` | `test_file_instance_shortcuts` | 84 | Distinct canonical regression case. |
| `tests/test_file_integration.py` | `test_file_move_and_rename_update_instance_path` | 87 | Distinct canonical regression case. |
| `tests/test_file_integration.py` | `test_file_copy_and_delete_via_instance` | 84 | Distinct canonical regression case. |
| `tests/test_file_integration.py` | `test_file_backup_and_hide_instance_wrappers` | 80 |  |
| `tests/test_file_integration.py` | `test_file_backup_empty_subdir` | 69 | Wall-clock dependence adds timing-flake risk. |
| `tests/test_file_integration.py` | `test_file_backup_hide_false` | 76 | Mock-heavy interaction check; limited real implementation coverage. Wall-clock dependence adds timing-flake risk. |
| `tests/test_file_integration.py` | `test_file_instance_wrappers` | 87 | Distinct canonical regression case. |
| `tests/test_file_integration.py` | `test_file_create_and_exists` | 86 | Distinct canonical regression case. |
| `tests/test_file_integration.py` | `test_file_backup_and_set_mod_time` | 73 | Wall-clock dependence adds timing-flake risk. |
| `tests/test_file_integration.py` | `test_file_get_encoding_and_read_write` | 84 | Distinct canonical regression case. |
| `tests/test_file_integration.py` | `test_file_format_size_and_size` | 77 | Distinct canonical regression case. |
| `tests/test_file_integration.py` | `test_file_get_extension_and_checksum` | 84 | Distinct canonical regression case. |
| `tests/test_file_integration.py` | `test_file_write_binary_and_text_paths` | 90 |  |
| `tests/test_file_integration.py` | `test_file_instance_move_and_rename` | 84 | Distinct canonical regression case. |
| `tests/test_file_integration.py` | `test_file_hide_unix` | 71 | Distinct canonical regression case. |
| `tests/test_file_integration.py` | `test_read_binary_mode_and_write_int` | 90 | Distinct canonical regression case. |
| `tests/test_file_integration.py` | `test_read_by_line_fallback_strip_control` | 78 | Distinct canonical regression case. |
| `tests/test_file_integration.py` | `test_file_instance_move_updates_path` | 74 | Distinct canonical regression case. |
| `tests/test_file_integration.py` | `test_file_copy_symlink` | 77 |  |
| `tests/test_file_integration.py` | `test_write_verbose_and_binary_mode` | 90 |  |
| `tests/test_file_integration.py` | `test_file_read_by_line_auto_detect_false` | 78 |  |
| `tests/test_file_integration.py` | `test_file_sha256_checksum` | 84 |  |
| `tests/test_file_integration.py` | `test_file_exist_and_format_size` | 77 |  |
| `tests/test_file_integration.py` | `test_file_wipe_truncates` | 84 |  |
| `tests/test_file_integration_negative.py` | `test_file_create_raises_on_existing` | 83 | Distinct canonical regression case. |
| `tests/test_file_integration_negative.py` | `test_file_move_nonexistent` | 86 | Distinct canonical regression case. |
| `tests/test_file_integration_negative.py` | `test_file_copy_nonexistent` | 86 | Distinct canonical regression case. |
| `tests/test_file_integration_negative.py` | `test_file_read_nonexistent` | 81 | Distinct canonical regression case. |
| `tests/test_file_integration_negative.py` | `test_file_wipe_nonexistent` | 81 | Distinct canonical regression case. |
| `tests/test_file_integration_negative.py` | `test_file_delete_directory_guard` | 83 | Distinct canonical regression case. |
| `tests/test_file_integration_negative.py` | `test_file_move_missing` | 86 | Distinct canonical regression case. |
| `tests/test_file_integration_negative.py` | `test_file_create_existing` | 78 | Re-scored after removing shadowing/stale-suite interference. |
| `tests/test_file_integration_negative.py` | `test_file_delete_directory` | 83 | Distinct canonical regression case. |
| `tests/test_file_integration_negative.py` | `test_file_delete_directory_raises` | 78 | Re-scored after removing shadowing/stale-suite interference. |
| `tests/test_file_integration_negative.py` | `test_file_move_conflict` | 77 |  |
| `tests/test_file_integration_negative.py` | `test_file_size_missing_raises` | 81 |  |
| `tests/test_file_integration_negative.py` | `test_file_get_encoding_invalid_path` | 75 | Distinct canonical regression case. |
| `tests/test_file_integration_negative.py` | `test_file_size_errors` | 75 |  |
| `tests/test_file_negative.py` | `test_file_create_raises_when_still_not_exists` | 77 | Distinct canonical regression case. |
| `tests/test_file_negative.py` | `test_file_delete_raises_when_not_deleted` | 77 | Distinct canonical regression case. |
| `tests/test_file_negative.py` | `test_file_backup_raises_when_backup_missing` | 80 | Distinct canonical regression case. |
| `tests/test_file_negative.py` | `test_file_instance_ensure_path_errors` | 84 | Distinct canonical regression case. |
| `tests/test_file_negative.py` | `test_file_delete_permission_error` | 80 |  |
| `tests/test_file_negative.py` | `test_file_copy_handles_permission` | 74 | Mock-heavy interaction check; limited real implementation coverage. |
| `tests/test_file_negative.py` | `test_file_read_permission_error` | 80 |  |
| `tests/test_file_negative.py` | `test_file_read_by_chunk_bad_mode` | 55 | Uses broad `pytest.raises(Exception)`; may pass for wrong failure reason. |
| `tests/test_file_negative.py` | `test_file_read_by_line_invalid_encoding` | 86 |  |
| `tests/test_file_negative.py` | `test_file_requires_path_before_actions` | 78 | Distinct canonical regression case. |
| `tests/test_file_negative.py` | `test_file_hide_unsupported` | 72 | Re-scored after removing shadowing/stale-suite interference. |
| `tests/test_file_negative.py` | `test_file_instance_delete_missing_path` | 81 | Distinct canonical regression case. |
| `tests/test_file_negative.py` | `test_file_create_invalid_verbose` | 81 | Distinct canonical regression case. |
| `tests/test_file_negative.py` | `test_file_read_invalid_mode` | 80 |  |
| `tests/test_funcs.py` | `test_q_repr_raises_systemexit` | 78 |  |
| `tests/test_funcs.py` | `test_dirify_basic` | 75 |  |
| `tests/test_funcs.py` | `test_dirify_with_wildcard` | 75 |  |
| `tests/test_funcs.py` | `test_multiple` | 79 |  |
| `tests/test_funcs.py` | `TestFuncsLegacyCoverage::test_q_call` | 78 | Re-scored after removing shadowing/stale-suite interference. |
| `tests/test_funcs.py` | `TestFuncsLegacyCoverage::test_q_call_with_code` | 78 | Re-scored after removing shadowing/stale-suite interference. |
| `tests/test_funcs.py` | `TestFuncsLegacyCoverage::test_dirify_type_error` | 72 | Re-scored after removing shadowing/stale-suite interference. |
| `tests/test_funcs.py` | `TestFuncsLegacyCoverage::test_dirify_attribute_error` | 72 | Re-scored after removing shadowing/stale-suite interference. |
| `tests/test_funcs.py` | `TestFuncsLegacyCoverage::test_dirify_os_error` | 72 | Re-scored after removing shadowing/stale-suite interference. |
| `tests/test_funcs.py` | `TestFuncsCoverage::test_dirify_handles_attribute_error` | 75 |  |
| `tests/test_funcs.py` | `TestFuncsCoverage::test_dirify_handles_os_error` | 75 |  |
| `tests/test_funcs.py` | `test_q_repr_exits` | 66 | Exact duplicate of `tests/test_funcs.py::test_q_repr_raises_systemexit`; redundant regression signal. |
| `tests/test_funcs.py` | `test_q_call_exits` | 72 |  |
| `tests/test_funcs.py` | `test_funcs_copy_and_paste_use_pyperclip` | 73 |  |
| `tests/test_funcs_integration.py` | `test_copy_paste` | 79 | Skipped in current environment; platform/dependency branch not runtime-verified here. |
| `tests/test_funcs_integration.py` | `TestFuncsCoverage::test_copy_and_paste_functions` | 79 | Distinct canonical regression case. |
| `tests/test_funcs_integration_negative.py` | — | 1 | No test functions; required matrix placeholder. |
| `tests/test_funcs_negative.py` | `test_dirify_nonexistent_attribute` | 75 | Distinct canonical regression case. |
| `tests/test_funcs_negative.py` | `test_dirify_empty_wildcard` | 82 | Distinct canonical regression case. |
| `tests/test_funcs_negative.py` | `test_multiple_with_no_types` | 78 | Distinct canonical regression case. |
| `tests/test_git.py` | `test_git9_import` | 50 | Valid public-export smoke test; weak behavioral signal. |
| `tests/test_git.py` | `test_git_callable_runs` | 66 | Mock-heavy interaction check; limited real implementation coverage. |
| `tests/test_git.py` | `TestGitLegacyCoverage::test_get_name_of_repo_special_case` | 73 | Re-scored after removing shadowing/stale-suite interference. |
| `tests/test_git.py` | `TestGitLegacyCoverage::test_get_name_of_repo_term` | 73 | Re-scored after removing shadowing/stale-suite interference. |
| `tests/test_git.py` | `TestGitLegacyCoverage::test_git_add_verbose` | 73 | Re-scored after removing shadowing/stale-suite interference. |
| `tests/test_git.py` | `TestGitLegacyCoverage::test_git_commit_with_message` | 76 | Re-scored after removing shadowing/stale-suite interference. |
| `tests/test_git.py` | `TestGitLegacyCoverage::test_git_instance_helpers` | 76 | Re-scored after removing shadowing/stale-suite interference. |
| `tests/test_git.py` | `TestGitLegacyCoverage::test_git_commit_verbose` | 73 | Re-scored after removing shadowing/stale-suite interference. |
| `tests/test_git.py` | `TestGitLegacyCoverage::test_git_push_with_upstream` | 76 | Re-scored after removing shadowing/stale-suite interference. |
| `tests/test_git.py` | `TestGitLegacyCoverage::test_git_push_verbose` | 73 | Re-scored after removing shadowing/stale-suite interference. |
| `tests/test_git.py` | `TestGitLegacyCoverage::test_git_update` | 76 | Re-scored after removing shadowing/stale-suite interference. |
| `tests/test_git.py` | `TestGitCoverage::test_call_with_remote_parameter_sets_remote` | 73 |  |
| `tests/test_git.py` | `TestGitCoverage::test_update_remote_uses_default_when_remote_not_set` | 66 | Mock-heavy interaction check; limited real implementation coverage. |
| `tests/test_git_integration.py` | — | 1 | No test functions; required matrix placeholder. |
| `tests/test_git_integration_negative.py` | — | 1 | No test functions; required matrix placeholder. |
| `tests/test_git_negative.py` | `test_git_callable_requires_message` | 78 | Distinct canonical regression case. |
| `tests/test_git_negative.py` | `TestGitCoverage::test_push_remote_raises_when_remote_not_set` | 78 | Distinct canonical regression case. |
| `tests/test_giv.py` | `test_giv9_import` | 50 | Valid public-export smoke test; weak behavioral signal. |
| `tests/test_giv_integration.py` | `TestGIVCoverage::test_setitem_and_getitem` | 65 | Verifies exact item assignment and retrieval behavior. |
| `tests/test_giv_integration.py` | `TestGIVCoverage::test_repr` | 72 | Distinct canonical regression case. |
| `tests/test_giv_integration.py` | `TestGIVCoverage::test_clean` | 72 | Distinct canonical regression case. |
| `tests/test_giv_integration.py` | `TestGIVCoverage::test_pop` | 82 | Distinct canonical regression case. |
| `tests/test_giv_integration.py` | `TestGIVCoverage::test_multiple_operations` | 82 | Distinct canonical regression case. |
| `tests/test_giv_integration.py` | `TestGIVCoverage::test_call_method_get` | 79 | Distinct canonical regression case. |
| `tests/test_giv_integration.py` | `TestGIVCoverage::test_call_method_set` | 79 | Distinct canonical regression case. |
| `tests/test_giv_integration.py` | `TestGIVCoverage::test_call_method_set_and_get` | 82 | Distinct canonical regression case. |
| `tests/test_giv_integration_negative.py` | `TestGIVCoverage::test_pop_with_default` | 79 | Distinct canonical regression case. |
| `tests/test_giv_negative.py` | — | 1 | No test functions; required matrix placeholder. |
| `tests/test_gui.py` | `test_gui9_import` | 50 | Valid public-export smoke test; weak behavioral signal. |
| `tests/test_gui.py` | `test_gui_instance_helper` | 66 |  |
| `tests/test_gui.py` | `test_gui_warning_macos_path` | 66 |  |
| `tests/test_gui.py` | `test_gui_warning_non_macos_alert` | 73 |  |
| `tests/test_gui.py` | `test_gui_warning_pypy_debug_path` | 66 |  |
| `tests/test_gui.py` | `test_gui_notification_macos` | 66 |  |
| `tests/test_gui.py` | `test_gui_warning_macos` | 66 |  |
| `tests/test_gui.py` | `test_gui_warning_instance_uses_stored_message` | 73 | Mock-heavy interaction check; limited real implementation coverage. |
| `tests/test_gui.py` | `test_gui_windows_notification_covers_on_destroy_and_loadimage_except` | 61 | Exercises private implementation detail; refactor-sensitive. |
| `tests/test_gui.py` | `test_gui_warning_sysargv_error` | 69 | Mock-heavy interaction check; limited real implementation coverage. |
| `tests/test_gui.py` | `test_gui_class_warning_pypy` | 73 | Re-scored after removing shadowing/stale-suite interference. |
| `tests/test_gui.py` | `test_gui_windows_notification_spawn` | 66 |  |
| `tests/test_gui.py` | `test_gui_notification_windows_retry_and_destroy` | 68 | Exercises private implementation detail; refactor-sensitive. |
| `tests/test_gui_integration.py` | — | 1 | No test functions; required matrix placeholder. |
| `tests/test_gui_integration_negative.py` | — | 1 | No test functions; required matrix placeholder. |
| `tests/test_gui_negative.py` | `test_gui_notify_raises_without_message` | 78 | Distinct canonical regression case. |
| `tests/test_gui_negative.py` | `test_gui_notify_not_implemented` | 72 | Distinct canonical regression case. |
| `tests/test_gui_negative.py` | `test_gui_warning_instance_missing_message_raises` | 81 | Distinct canonical regression case. |
| `tests/test_gui_negative.py` | `test_gui_notify_instance_missing_message` | 81 | Distinct canonical regression case. |
| `tests/test_gui_negative.py` | `test_gui_notification_unsupported` | 72 |  |
| `tests/test_gui_negative.py` | `test_gui_warning_missing_message` | 75 |  |
| `tests/test_id.py` | `test_id_starts_at_zero` | 79 |  |
| `tests/test_id.py` | `test_id_increments` | 82 |  |
| `tests/test_id.py` | `test_id_multiple_instances` | 82 |  |
| `tests/test_id.py` | `test_id_many_increments` | 79 |  |
| `tests/test_id.py` | `test_id_call_method` | 82 |  |
| `tests/test_id.py` | `test_id_call_vs_get` | 82 |  |
| `tests/test_id_integration.py` | — | 1 | No test functions; required matrix placeholder. |
| `tests/test_id_integration_negative.py` | — | 1 | No test functions; required matrix placeholder. |
| `tests/test_id_negative.py` | — | 1 | No test functions; required matrix placeholder. |
| `tests/test_instance.py` | `test_add_instance_shortcuts_adds_getattr` | 79 |  |
| `tests/test_instance.py` | `test_add_instance_shortcuts_non_callable_attr` | 72 |  |
| `tests/test_instance.py` | `test_add_instance_shortcuts_delegate_called` | 79 |  |
| `tests/test_instance_integration.py` | — | 1 | No test functions; required matrix placeholder. |
| `tests/test_instance_integration_negative.py` | — | 1 | No test functions; required matrix placeholder. |
| `tests/test_instance_negative.py` | `TestInstanceCoverage::test_delegate_raises_attribute_error_for_non_callable` | 81 | Distinct canonical regression case. |
| `tests/test_int.py` | `TestIntFromTo::test_from_to_basic` | 79 |  |
| `tests/test_int.py` | `TestIntFromTo::test_from_to_negative` | 82 |  |
| `tests/test_int.py` | `TestIntFromTo::test_from_to_single` | 79 |  |
| `tests/test_int.py` | `TestIntFromTo::test_from_to_to_str` | 79 |  |
| `tests/test_int.py` | `TestIntFromTo::test_from_to_to_str_padded` | 79 |  |
| `tests/test_int.py` | `TestIntFromTo::test_from_to_to_str_negative` | 82 |  |
| `tests/test_int.py` | `TestIntFromTo::test_from_to_large_range` | 82 |  |
| `tests/test_int.py` | `TestIntFromTo::test_from_to_returns_range` | 55 | Valid narrow contract. Only type/presence assertion; behavioral regression coverage is weak. |
| `tests/test_int.py` | `TestIntFromTo::test_from_to_reversed_range` | 72 |  |
| `tests/test_int.py` | `TestIntFromTo::test_from_to_very_large_range` | 82 |  |
| `tests/test_int.py` | `TestIntFromTo::test_from_to_extreme_negative` | 82 |  |
| `tests/test_int.py` | `TestIntFromTo::test_from_to_zero_crossing` | 79 |  |
| `tests/test_int.py` | `TestIntFromTo::test_int_instance_shortcut` | 79 |  |
| `tests/test_int.py` | `test_int_instance_range` | 79 |  |
| `tests/test_int.py` | `TestIntInstance::test_int_instance_init_both_params` | 55 | Narrow constructor/property state check. |
| `tests/test_int.py` | `TestIntInstance::test_int_instance_init_none` | 55 | Valid narrow contract. Narrow constructor/property state check. |
| `tests/test_int.py` | `TestIntInstance::test_int_instance_init_partial` | 55 | Narrow constructor/property state check. |
| `tests/test_int.py` | `TestIntInstance::test_int_instance_range_basic` | 79 |  |
| `tests/test_int.py` | `TestIntInstance::test_int_instance_range_to_str` | 79 |  |
| `tests/test_int.py` | `TestIntInstance::test_int_instance_range_negative` | 82 |  |
| `tests/test_int.py` | `TestIntInstance::test_int_instance_range_negative_to_str` | 75 |  |
| `tests/test_int.py` | `TestIntInstance::test_int_instance_range_single_value` | 79 |  |
| `tests/test_int.py` | `TestIntInstance::test_int_instance_range_reversed` | 79 |  |
| `tests/test_int_integration.py` | — | 1 | No test functions; required matrix placeholder. |
| `tests/test_int_integration_negative.py` | — | 1 | No test functions; required matrix placeholder. |
| `tests/test_int_negative.py` | `TestIntInstance::test_int_instance_ensure_raises_no_start` | 70 | Exercises private implementation detail; refactor-sensitive. |
| `tests/test_int_negative.py` | `TestIntInstance::test_int_instance_ensure_raises_no_end` | 70 | Exercises private implementation detail; refactor-sensitive. |
| `tests/test_int_negative.py` | `TestIntInstance::test_int_instance_ensure_raises_both_none` | 70 | Exercises private implementation detail; refactor-sensitive. |
| `tests/test_int_negative.py` | `TestIntInstance::test_int_instance_range_raises_without_params` | 78 | Distinct canonical regression case. |
| `tests/test_json.py` | `TestJsonCoverage::test_json_call_without_args_returns_string` | 79 |  |
| `tests/test_json.py` | `TestJsonCoverage::test_jsondict_call_without_args_returns_string` | 79 |  |
| `tests/test_json.py` | `TestJsonCoverage::test_jsonlist_call_without_args_returns_string` | 79 |  |
| `tests/test_json.py` | `TestJsonCoverage::test_jsonlist_call_with_value_appends` | 84 |  |
| `tests/test_json.py` | `TestJsonCoverage::test_jsondict_file_exists_error_during_create` | 81 |  |
| `tests/test_json_integration.py` | `test_json_create_new_file` | 84 | Distinct canonical regression case. |
| `tests/test_json_integration.py` | `test_json_save_and_load` | 84 | Distinct canonical regression case. |
| `tests/test_json_integration.py` | `test_json_len` | 84 | Distinct canonical regression case. |
| `tests/test_json_integration.py` | `test_json_contains` | 77 | Distinct canonical regression case. |
| `tests/test_json_integration.py` | `test_jsondict_getitem_setitem` | 84 | Distinct canonical regression case. |
| `tests/test_json_integration.py` | `test_jsondict_items_keys_values` | 87 | Distinct canonical regression case. |
| `tests/test_json_integration.py` | `test_jsondict_clear` | 84 | Distinct canonical regression case. |
| `tests/test_json_integration.py` | `test_jsonlist_append` | 84 | Distinct canonical regression case. |
| `tests/test_json_integration.py` | `test_jsonlist_getitem_setitem` | 84 | Distinct canonical regression case. |
| `tests/test_json_integration.py` | `test_jsonlist_index` | 84 | Distinct canonical regression case. |
| `tests/test_json_integration.py` | `test_jsonlist_sort` | 84 | Distinct canonical regression case. |
| `tests/test_json_integration.py` | `test_jsonlist_clear` | 84 | Distinct canonical regression case. |
| `tests/test_json_integration.py` | `test_json_unicode` | 87 | Distinct canonical regression case. |
| `tests/test_json_integration.py` | `test_json_repr` | 77 | Distinct canonical regression case. |
| `tests/test_json_integration.py` | `test_json_pop` | 84 | Distinct canonical regression case. |
| `tests/test_json_integration.py` | `test_json_save_debug` | 77 | Distinct canonical regression case. |
| `tests/test_json_integration.py` | `test_json_save_not_quiet` | 77 | Distinct canonical regression case. |
| `tests/test_json_integration.py` | `test_json_callable_save_and_get` | 84 | Distinct canonical regression case. |
| `tests/test_json_integration.py` | `test_json_load_empty_file` | 87 | Distinct canonical regression case. |
| `tests/test_json_integration.py` | `test_json_load_not_quiet` | 77 | Distinct canonical regression case. |
| `tests/test_json_integration.py` | `test_json_load_debug` | 77 | Distinct canonical regression case. |
| `tests/test_json_integration.py` | `test_jsondict_iter` | 84 | Distinct canonical regression case. |
| `tests/test_json_integration.py` | `test_jsondict_str` | 77 | Distinct canonical regression case. |
| `tests/test_json_integration.py` | `test_jsondict_callable_set_get_save` | 84 | Distinct canonical regression case. |
| `tests/test_json_integration.py` | `test_jsonlist_str` | 77 | Distinct canonical regression case. |
| `tests/test_json_integration.py` | `test_jsonlist_callable_append_save` | 84 | Distinct canonical regression case. |
| `tests/test_json_integration_negative.py` | `test_jsondict_raises_on_non_dict` | 83 | Distinct canonical regression case. |
| `tests/test_json_integration_negative.py` | `test_jsonlist_raises_on_non_list` | 83 | Distinct canonical regression case. |
| `tests/test_json_integration_negative.py` | `test_jsondict_getitem_missing_key` | 86 | Distinct canonical regression case. |
| `tests/test_json_integration_negative.py` | `test_jsonlist_index_not_found` | 83 | Distinct canonical regression case. |
| `tests/test_json_integration_negative.py` | `test_jsonlist_index_out_of_range` | 83 | Distinct canonical regression case. |
| `tests/test_json_integration_negative.py` | `test_json_corrupted_file` | 55 | Uses broad `pytest.raises(Exception)`; may pass for wrong failure reason. |
| `tests/test_json_negative.py` | — | 1 | No test functions; required matrix placeholder. |
| `tests/test_keyboard.py` | `test_keyboard9_import` | 50 | Valid public-export smoke test; weak behavioral signal. |
| `tests/test_keyboard.py` | `TestKeyboardCoverage::test_hotkey_with_verbose` | 66 |  |
| `tests/test_keyboard.py` | `TestKeyboardCoverage::test_hotkey_without_verbose` | 73 | Mock-heavy interaction check; limited real implementation coverage. |
| `tests/test_keyboard.py` | `TestKeyboardCoverage::test_translate_cyrillic_to_qwerty` | 82 |  |
| `tests/test_keyboard.py` | `TestKeyboardCoverage::test_translate_special_characters` | 82 |  |
| `tests/test_keyboard.py` | `TestKeyboardCoverage::test_translate_uppercase_cyrillic` | 82 |  |
| `tests/test_keyboard.py` | `TestKeyboardCoverage::test_keyboard_instance_helpers` | 66 | Mock-heavy interaction check; limited real implementation coverage. |
| `tests/test_keyboard.py` | `TestKeyboardCoverage::test_translate_unmapped_characters` | 82 |  |
| `tests/test_keyboard.py` | `TestKeyboardCoverage::test_translate_string_basic` | 79 |  |
| `tests/test_keyboard.py` | `TestKeyboardCoverage::test_translate_string_mixed` | 79 |  |
| `tests/test_keyboard.py` | `TestKeyboardCoverage::test_translate_string_empty` | 82 |  |
| `tests/test_keyboard.py` | `TestKeyboardCoverage::test_write_with_verbose` | 69 |  |
| `tests/test_keyboard.py` | `TestKeyboardCoverage::test_write_without_verbose` | 73 |  |
| `tests/test_keyboard.py` | `test_keyboard_translate_mapping` | 82 |  |
| `tests/test_keyboard.py` | `test_keyboard_translate_string` | 79 |  |
| `tests/test_keyboard.py` | `test_keyboard_write_and_hotkey` | 76 |  |
| `tests/test_keyboard.py` | `test_keyboard_instance_helpers` | 73 |  |
| `tests/test_keyboard.py` | `test_keyboard_hotkey_verbose_prints` | 66 |  |
| `tests/test_keyboard.py` | `test_keyboard_write_verbose_prints` | 66 |  |
| `tests/test_keyboard_integration.py` | — | 1 | No test functions; required matrix placeholder. |
| `tests/test_keyboard_integration_negative.py` | — | 1 | No test functions; required matrix placeholder. |
| `tests/test_keyboard_negative.py` | — | 1 | No test functions; required matrix placeholder. |
| `tests/test_list.py` | `TestListFlatterize::test_flatterize_basic` | 79 |  |
| `tests/test_list.py` | `TestListFlatterize::test_flatterize_nested` | 79 |  |
| `tests/test_list.py` | `TestListFlatterize::test_flatterize_tuple` | 79 |  |
| `tests/test_list.py` | `TestListSplitEvery::test_split_every_basic` | 79 |  |
| `tests/test_list.py` | `TestListSplitEvery::test_split_every_uneven` | 79 |  |
| `tests/test_list.py` | `TestListSplitEvery::test_split_every_zero` | 79 |  |
| `tests/test_list.py` | `TestListSplitEvery::test_split_every_larger_than_list` | 79 |  |
| `tests/test_list.py` | `TestListSplitEvery::test_split_every_single_element` | 79 |  |
| `tests/test_list.py` | `TestListWildcardSearch::test_wildcard_search_star` | 79 |  |
| `tests/test_list.py` | `TestListWildcardSearch::test_wildcard_search_question` | 79 |  |
| `tests/test_list.py` | `TestListWildcardSearch::test_wildcard_search_combined` | 79 |  |
| `tests/test_list.py` | `TestListWildcardSearch::test_wildcard_search_no_match` | 79 |  |
| `tests/test_list.py` | `TestListReplaceString::test_replace_string_basic` | 79 |  |
| `tests/test_list.py` | `TestListReplaceString::test_replace_string_integers` | 79 |  |
| `tests/test_list.py` | `TestListReplaceString::test_replace_string_no_match` | 79 |  |
| `tests/test_list.py` | `TestListApplyLambda::test_apply_lambda_basic` | 79 |  |
| `tests/test_list.py` | `TestListApplyLambda::test_apply_lambda_string_upper` | 79 |  |
| `tests/test_list.py` | `TestListToStrings::test_to_strings_mixed_types` | 79 |  |
| `tests/test_list.py` | `TestListToStrings::test_to_strings_already_strings` | 79 |  |
| `tests/test_list.py` | `TestListRemoveDuplicates::test_remove_duplicates_preserve_order` | 79 |  |
| `tests/test_list.py` | `TestListRemoveDuplicates::test_remove_duplicates_no_preserve_order` | 79 |  |
| `tests/test_list.py` | `TestListRemoveDuplicates::test_remove_duplicates_no_duplicates` | 79 |  |
| `tests/test_list.py` | `TestListRemoveDuplicates::test_remove_duplicates_strings` | 79 |  |
| `tests/test_list.py` | `TestListMostCommon::test_most_common_basic` | 79 |  |
| `tests/test_list.py` | `TestListMostCommon::test_most_common_strings` | 79 |  |
| `tests/test_list.py` | `TestListMostCommon::test_most_common_single` | 79 |  |
| `tests/test_list.py` | `TestListShuffle::test_shuffle_preserves_elements` | 79 |  |
| `tests/test_list.py` | `TestListShuffle::test_shuffle_doesnt_modify_original` | 79 |  |
| `tests/test_list.py` | `TestListShuffle::test_shuffle_different_results` | 72 |  |
| `tests/test_list.py` | `TestListRemoveEmptyStrings::test_remove_empty_strings_basic` | 75 |  |
| `tests/test_list.py` | `TestListRemoveEmptyStrings::test_remove_empty_strings_no_empty` | 82 |  |
| `tests/test_list.py` | `TestListRemoveEmptyStrings::test_remove_empty_strings_all_empty` | 82 |  |
| `tests/test_list.py` | `TestListSortBy::test_sort_by_single_key` | 79 |  |
| `tests/test_list.py` | `TestListSortBy::test_sort_by_multiple_keys` | 82 |  |
| `tests/test_list.py` | `TestListEnumBy::test_enum_by_basic` | 79 |  |
| `tests/test_list.py` | `TestListEnumBy::test_enum_by_dict_list` | 79 |  |
| `tests/test_list.py` | `TestListNegative::test_flatterize_empty_list` | 82 |  |
| `tests/test_list.py` | `TestListNegative::test_flatterize_deeply_nested` | 55 | Valid narrow contract. Only type/presence assertion; behavioral regression coverage is weak. |
| `tests/test_list.py` | `TestListNegative::test_split_every_empty_list` | 55 | Valid narrow contract. Only type/presence assertion; behavioral regression coverage is weak. |
| `tests/test_list.py` | `TestListNegative::test_split_every_negative` | 55 | Valid narrow contract. Only type/presence assertion; behavioral regression coverage is weak. |
| `tests/test_list.py` | `TestListNegative::test_wildcard_search_empty_list` | 82 |  |
| `tests/test_list.py` | `TestListNegative::test_wildcard_search_empty_pattern` | 55 | Valid narrow contract. Only type/presence assertion; behavioral regression coverage is weak. |
| `tests/test_list.py` | `TestListNegative::test_apply_lambda_empty_list` | 82 |  |
| `tests/test_list.py` | `TestListNegative::test_most_common_empty_list` | 82 |  |
| `tests/test_list.py` | `TestListNegative::test_most_common_zero_count` | 79 |  |
| `tests/test_list.py` | `TestListNegative::test_shuffle_empty_list` | 82 |  |
| `tests/test_list.py` | `TestListNegative::test_enum_by_empty_list` | 82 |  |
| `tests/test_list.py` | `TestListCoverage::test_itemgetter_with_casting_non_iterable_cast_to` | 55 | Narrow constructor/property state check. |
| `tests/test_list.py` | `TestListCoverage::test_itemgetter_with_casting_single_item_fallback` | 79 |  |
| `tests/test_list.py` | `TestListCoverage::test_itemgetter_with_casting_multiple_items_fallback` | 82 |  |
| `tests/test_list.py` | `TestListCoverage::test_itemgetter_with_casting_multiple_cast_types` | 79 |  |
| `tests/test_list.py` | `TestListCoverage::test_enum_by_with_cast_to` | 79 |  |
| `tests/test_list.py` | `TestListCoverage::test_sort_by_with_cast_to_tuple` | 82 |  |
| `tests/test_list.py` | `test_list_instance_helpers` | 82 |  |
| `tests/test_list.py` | `test_list_callable_returns_data` | 79 |  |
| `tests/test_list.py` | `TestListInstance::test_list_instance_init_none` | 55 | Valid narrow contract. Narrow constructor/property state check. |
| `tests/test_list.py` | `TestListInstance::test_list_instance_init_with_data` | 55 | Narrow constructor/property state check. |
| `tests/test_list.py` | `TestListInstance::test_list_instance_call_with_data` | 79 |  |
| `tests/test_list.py` | `TestListInstance::test_list_instance_call_with_none` | 55 | Valid narrow contract. Only type/presence assertion; behavioral regression coverage is weak. |
| `tests/test_list.py` | `TestListInstance::test_list_instance_flatterize_forwarding` | 79 |  |
| `tests/test_list.py` | `TestListInstance::test_list_instance_split_every_forwarding` | 79 |  |
| `tests/test_list.py` | `TestListInstance::test_list_instance_shuffle_forwarding` | 79 |  |
| `tests/test_list.py` | `TestListInstance::test_list_instance_remove_duplicates_forwarding` | 79 |  |
| `tests/test_list.py` | `TestListInstance::test_list_instance_remove_duplicates_no_order` | 82 |  |
| `tests/test_list.py` | `TestListInstance::test_list_instance_getattribute_non_forwarded` | 82 |  |
| `tests/test_list.py` | `TestListInstance::test_list_instance_multiple_operations` | 82 |  |
| `tests/test_list.py` | `test_list_enum_by_cast_to_breaks_on_success` | 79 |  |
| `tests/test_list_integration.py` | — | 1 | No test functions; required matrix placeholder. |
| `tests/test_list_integration_negative.py` | — | 1 | No test functions; required matrix placeholder. |
| `tests/test_list_negative.py` | `TestListFlatterize::test_flatterize_invalid_type` | 81 | Distinct canonical regression case. |
| `tests/test_list_negative.py` | `TestListNegative::test_apply_lambda_exception` | 55 | Uses broad `pytest.raises(Exception)`; may pass for wrong failure reason. |
| `tests/test_list_negative.py` | `TestListNegative::test_sort_by_missing_key` | 70 | Requires KeyError for a missing sort key. |
| `tests/test_list_negative.py` | `TestListNegative::test_enum_by_invalid_key` | 70 | Requires KeyError for a missing enumeration key. |
| `tests/test_list_negative.py` | `test_list_callable_raises_without_data` | 78 | Distinct canonical regression case. |
| `tests/test_list_negative.py` | `TestListInstance::test_list_instance_ensure_raises` | 70 | Exercises private implementation detail; refactor-sensitive. |
| `tests/test_list_negative.py` | `TestListInstance::test_list_instance_none_data_raises_on_forward` | 81 | Distinct canonical regression case. |
| `tests/test_log.py` | `test_logger_exists` | 55 | Valid narrow contract. Only type/presence assertion; behavioral regression coverage is weak. |
| `tests/test_log.py` | `test_logger_is_class` | 55 | Valid narrow contract. Only type/presence assertion; behavioral regression coverage is weak. |
| `tests/test_log_integration.py` | — | 1 | No test functions; required matrix placeholder. |
| `tests/test_log_integration_negative.py` | — | 1 | No test functions; required matrix placeholder. |
| `tests/test_log_negative.py` | — | 1 | No test functions; required matrix placeholder. |
| `tests/test_macos.py` | `test_os_name_linux_branch` | 73 | Distinct canonical regression case. |
| `tests/test_macos.py` | `test_path_temp_non_macos` | 73 | Distinct canonical regression case. |
| `tests/test_macos.py` | `test_macos9_import` | 50 | Valid public-export smoke test; weak behavioral signal. |
| `tests/test_macos.py` | `test_macos_callable_sets_message` | 73 | Mock-heavy interaction check; limited real implementation coverage. |
| `tests/test_macos.py` | `test_macos_instance_helper` | 66 |  |
| `tests/test_macos.py` | `test_macos_osascript_escape` | 72 |  |
| `tests/test_macos.py` | `test_macos_notification_builds_command` | 66 |  |
| `tests/test_macos.py` | `test_macos_instance_call_updates_fields_and_calls_notification` | 73 |  |
| `tests/test_macos.py` | `test_macos_get_list_of_sounds_verbose` | 69 |  |
| `tests/test_macos.py` | `test_macos_symlink_calls_ln` | 73 |  |
| `tests/test_macos_integration.py` | `test_dir_copy_symlink_lchmod_failure` | 71 | Distinct canonical regression case. |
| `tests/test_macos_integration.py` | `test_file_get_mime_non_windows` | 78 | Distinct canonical regression case. |
| `tests/test_macos_integration_negative.py` | — | 1 | No test functions; required matrix placeholder. |
| `tests/test_macos_negative.py` | `test_macos_callable_requires_message` | 78 | Distinct canonical regression case. |
| `tests/test_main.py` | `test_commands_main_import` | 50 | Valid public-export smoke test; weak behavioral signal. |
| `tests/test_main_integration.py` | — | 1 | No test functions; required matrix placeholder. |
| `tests/test_main_integration_negative.py` | — | 1 | No test functions; required matrix placeholder. |
| `tests/test_main_negative.py` | — | 1 | No test functions; required matrix placeholder. |
| `tests/test_module.py` | `test_lazy_module_sys_modules_override` | 76 |  |
| `tests/test_module.py` | `test_lazy_module_overrides_and_delete` | 85 |  |
| `tests/test_module.py` | `test_lazy_module_dir_optional_missing` | 82 |  |
| `tests/test_module.py` | `test_lazy_property_repr_and_call` | 82 |  |
| `tests/test_module.py` | `test_lazy_property_bin_ops` | 82 |  |
| `tests/test_module.py` | `test_lazy_property_attr_set_del` | 76 |  |
| `tests/test_module_integration.py` | — | 1 | No test functions; required matrix placeholder. |
| `tests/test_module_integration_negative.py` | — | 1 | No test functions; required matrix placeholder. |
| `tests/test_module_negative.py` | `test_lazy_module_optional_missing` | 81 |  |
| `tests/test_mouse.py` | `test_mouse9_import` | 50 | Valid public-export smoke test; weak behavioral signal. |
| `tests/test_mouse.py` | `TestMouseLegacyCoverage::test_set_mouse_move_duration` | 79 | Re-scored after removing shadowing/stale-suite interference. |
| `tests/test_mouse.py` | `TestMouseLegacyCoverage::test_scroll_up` | 76 | Re-scored after removing shadowing/stale-suite interference. |
| `tests/test_mouse.py` | `TestMouseLegacyCoverage::test_scroll_down` | 73 | Re-scored after removing shadowing/stale-suite interference. |
| `tests/test_mouse.py` | `TestMouseLegacyCoverage::test_scroll_up_method` | 73 | Re-scored after removing shadowing/stale-suite interference. |
| `tests/test_mouse.py` | `TestMouseLegacyCoverage::test_scroll_down_method` | 73 | Re-scored after removing shadowing/stale-suite interference. |
| `tests/test_mouse.py` | `TestMouseLegacyCoverage::test_click_with_position_verbose_false` | 76 | Re-scored after removing shadowing/stale-suite interference. |
| `tests/test_mouse.py` | `TestMouseLegacyCoverage::test_click_without_position` | 73 | Re-scored after removing shadowing/stale-suite interference. |
| `tests/test_mouse.py` | `TestMouseLegacyCoverage::test_click_right` | 76 | Re-scored after removing shadowing/stale-suite interference. |
| `tests/test_mouse.py` | `TestMouseLegacyCoverage::test_click_left` | 73 | Re-scored after removing shadowing/stale-suite interference. |
| `tests/test_mouse.py` | `TestMouseLegacyCoverage::test_click_middle` | 73 | Re-scored after removing shadowing/stale-suite interference. |
| `tests/test_mouse.py` | `TestMouseLegacyCoverage::test_move_basic` | 76 | Re-scored after removing shadowing/stale-suite interference. |
| `tests/test_mouse.py` | `TestMouseLegacyCoverage::test_move_tuple_2_elements` | 73 | Re-scored after removing shadowing/stale-suite interference. |
| `tests/test_mouse.py` | `TestMouseLegacyCoverage::test_move_tuple_4_elements` | 73 | Re-scored after removing shadowing/stale-suite interference. |
| `tests/test_mouse.py` | `TestMouseLegacyCoverage::test_move_with_x2_y2` | 73 | Re-scored after removing shadowing/stale-suite interference. |
| `tests/test_mouse.py` | `TestMouseLegacyCoverage::test_move_relative` | 76 | Re-scored after removing shadowing/stale-suite interference. |
| `tests/test_mouse.py` | `TestMouseLegacyCoverage::test_get_position` | 73 | Re-scored after removing shadowing/stale-suite interference. |
| `tests/test_mouse.py` | `TestMouseCoverage::test_mouse_init` | 55 | Valid narrow contract. Narrow constructor/property state check. |
| `tests/test_mouse.py` | `TestMouseCoverage::test_mouse_instance_scroll` | 66 | Re-scored after removing shadowing/stale-suite interference. |
| `tests/test_mouse.py` | `TestMouseCoverage::test_mouse_instance_click` | 66 | Re-scored after removing shadowing/stale-suite interference. |
| `tests/test_mouse.py` | `TestMouseCoverage::test_mouse_instance_move_to` | 66 | Re-scored after removing shadowing/stale-suite interference. |
| `tests/test_mouse.py` | `TestMouseCoverage::test_mouse_instance_position` | 73 |  |
| `tests/test_mouse_integration.py` | — | 1 | No test functions; required matrix placeholder. |
| `tests/test_mouse_integration_negative.py` | — | 1 | No test functions; required matrix placeholder. |
| `tests/test_mouse_negative.py` | — | 1 | No test functions; required matrix placeholder. |
| `tests/test_network.py` | `test_network_get_domain_of_url` | 82 |  |
| `tests/test_network.py` | `test_network_get_protocol_of_url` | 82 |  |
| `tests/test_network.py` | `TestNetworkCoverage::test_get_domain_edge_cases` | 85 |  |
| `tests/test_network.py` | `TestNetworkCoverage::test_get_fqdn_no_ip` | 79 |  |
| `tests/test_network.py` | `TestNetworkCoverage::test_get_fqdn_with_ip` | 55 | Valid narrow contract. Only type/presence assertion; behavioral regression coverage is weak. |
| `tests/test_network.py` | `TestNetworkCoverage::test_get_netbios` | 79 |  |
| `tests/test_network.py` | `TestNetworkCoverage::test_ping_quiet` | 55 | Valid narrow contract. Only type/presence assertion; behavioral regression coverage is weak. |
| `tests/test_network.py` | `TestNetworkCoverage::test_ping_verbose` | 66 |  |
| `tests/test_network.py` | `TestNetworkCoverage::test_ping_multiple_count` | 55 | Valid narrow contract. Only type/presence assertion; behavioral regression coverage is weak. |
| `tests/test_network.py` | `TestNetworkCoverage::test_download_file_with_out` | 71 |  |
| `tests/test_network.py` | `TestNetworkCoverage::test_download_file_auto_name` | 55 | Valid narrow contract. Only type/presence assertion; behavioral regression coverage is weak. |
| `tests/test_network.py` | `TestNetworkCoverage::test_get_global_ip_fast` | 66 |  |
| `tests/test_network.py` | `TestNetworkCoverage::test_check_response_bytes` | 55 | Valid narrow contract. Only type/presence assertion; behavioral regression coverage is weak. |
| `tests/test_network.py` | `TestNetworkCoverage::test_check_response_string` | 55 | Valid narrow contract. Only type/presence assertion; behavioral regression coverage is weak. |
| `tests/test_network.py` | `TestNetworkCoverage::test_check_response_list` | 55 | Valid narrow contract. Only type/presence assertion; behavioral regression coverage is weak. |
| `tests/test_network.py` | `TestNetworkCoverage::test_check_response_connection_error` | 69 |  |
| `tests/test_network.py` | `TestNetworkCoverage::test_check_response_debug` | 55 | Valid narrow contract. Only type/presence assertion; behavioral regression coverage is weak. |
| `tests/test_network.py` | `TestNetworkCoverage::test_check_internet_apple` | 55 | Valid narrow contract. Only type/presence assertion; behavioral regression coverage is weak. |
| `tests/test_network.py` | `TestNetworkCoverage::test_check_internet_microsoft` | 55 | Valid narrow contract. Only type/presence assertion; behavioral regression coverage is weak. |
| `tests/test_network.py` | `TestNetworkCoverage::test_check_internet_microsoft_connect` | 55 | Valid narrow contract. Only type/presence assertion; behavioral regression coverage is weak. |
| `tests/test_network.py` | `TestNetworkCoverage::test_check_internet_google` | 55 | Valid narrow contract. Only type/presence assertion; behavioral regression coverage is weak. |
| `tests/test_network.py` | `TestNetworkCoverage::test_check_internet_firefox` | 55 | Valid narrow contract. Only type/presence assertion; behavioral regression coverage is weak. |
| `tests/test_network.py` | `TestNetworkCoverage::test_request_get` | 73 |  |
| `tests/test_network.py` | `TestNetworkCoverage::test_request_get_with_auth` | 76 | Re-scored after removing shadowing/stale-suite interference. |
| `tests/test_network.py` | `TestNetworkCoverage::test_request_unsupported_method` | 78 |  |
| `tests/test_network.py` | `TestNetworkCoverage::test_get_wrapper` | 73 |  |
| `tests/test_network.py` | `TestNetworkCoverage::test_ping_failure` | 66 |  |
| `tests/test_network.py` | `TestNetworkCoverage::test_get_netbios_with_ip` | 73 |  |
| `tests/test_network.py` | `TestNetworkCoverage::test_get_global_ip_slow_mode` | 66 |  |
| `tests/test_network.py` | `TestNetworkCoverage::test_check_response_invalid_type` | 81 |  |
| `tests/test_network.py` | `TestNetworkCoverage::test_check_response_debug_connection_error` | 69 |  |
| `tests/test_network.py` | `TestNetworkCoverage::test_check_internet_google_debug` | 55 | Valid narrow contract. Only type/presence assertion; behavioral regression coverage is weak. |
| `tests/test_network.py` | `TestNetworkCoverage::test_network_instance_helpers` | 76 |  |
| `tests/test_network.py` | `TestNetworkCoverage::test_check_internet_google_connection_error` | 69 |  |
| `tests/test_network.py` | `TestNetworkCoverage::test_request_post_with_json` | 73 |  |
| `tests/test_network.py` | `test_network_download_file_monkeypatched` | 70 | Exercises private implementation detail; refactor-sensitive. |
| `tests/test_network.py` | `test_network_get_netbios` | 73 |  |
| `tests/test_network.py` | `test_network_check_internet_wrappers` | 69 |  |
| `tests/test_network.py` | `test_network_get_global_ip_slow_not_found` | 72 |  |
| `tests/test_network.py` | `test_network_class_ping_defaults` | 72 |  |
| `tests/test_network.py` | `test_network_class_get_fqdn_accepts_optional` | 55 | Valid narrow contract. Only type/presence assertion; behavioral regression coverage is weak. |
| `tests/test_network.py` | `test_network_call_sets_target_and_params` | 76 |  |
| `tests/test_network.py` | `test_network_instance_ping_uses_stored_target` | 76 | Mock-heavy interaction check; limited real implementation coverage. |
| `tests/test_network.py` | `test_network_instance_methods_use_target` | 76 |  |
| `tests/test_network.py` | `test_network_download_file_default_out` | 81 |  |
| `tests/test_network.py` | `test_network_check_internet_google_debug_not_output` | 66 |  |
| `tests/test_network.py` | `test_network_get_global_ip_fast_success_utf8` | 70 | Exercises private implementation detail; refactor-sensitive. |
| `tests/test_network.py` | `test_network_get_global_ip_fast_decode_iso_fallback` | 78 |  |
| `tests/test_network.py` | `test_network_get_global_ip_fast_all_fail_returns_empty` | 81 |  |
| `tests/test_network.py` | `test_network_get_global_ip_slow_verbose_most_frequent` | 70 | Exercises private implementation detail; refactor-sensitive. |
| `tests/test_network.py` | `test_network_ping_verbose_up_multiple` | 69 |  |
| `tests/test_network.py` | `test_network_ping_verbose_down_returns_false` | 66 |  |
| `tests/test_network.py` | `test_network_get_netbios_with_ip_calls_hostbyaddr` | 73 |  |
| `tests/test_network.py` | `test_network_request_routes_and_auth` | 82 |  |
| `tests/test_network.py` | `test_network_check_response_success` | 66 |  |
| `tests/test_network.py` | `test_network_check_response_failure_debug` | 66 |  |
| `tests/test_network.py` | `test_network_check_internet_google_paths` | 66 |  |
| `tests/test_network_integration.py` | `test_network_get_ip` | 72 | Distinct canonical regression case. |
| `tests/test_network_integration_negative.py` | `test_network_get_ip_invalid_domain` | 82 | Distinct canonical regression case. |
| `tests/test_network_negative.py` | `TestNetworkMissingCoverage::test_instance_ping_no_target` | 78 | Distinct canonical regression case. |
| `tests/test_network_negative.py` | `TestNetworkMissingCoverage::test_instance_get_ip_no_target` | 78 | Distinct canonical regression case. |
| `tests/test_network_negative.py` | `TestNetworkMissingCoverage::test_instance_get_fqdn_no_target` | 78 | Distinct canonical regression case. |
| `tests/test_network_negative.py` | `TestNetworkMissingCoverage::test_ping_keyboard_interrupt` | 72 | Distinct canonical regression case. |
| `tests/test_network_negative.py` | `TestNetworkMissingCoverage::test_ping_exception_handling` | 66 | Distinct canonical regression case. |
| `tests/test_network_negative.py` | `TestNetworkMissingCoverage::test_ping_missing_os_ping` | 69 |  |
| `tests/test_network_negative.py` | `TestNetworkMissingCoverage::test_check_response_debug_no_output` | 69 | Distinct canonical regression case. |
| `tests/test_network_negative.py` | `test_network_get_protocol_of_url_raises` | 78 | Distinct canonical regression case. |
| `tests/test_network_negative.py` | `test_network_get_protocol_of_url_no_protocol` | 78 | Distinct canonical regression case. |
| `tests/test_network_negative.py` | `test_network_get_protocol_of_url_invalid` | 81 | Distinct canonical regression case. |
| `tests/test_network_negative.py` | `test_network_callable_missing_target` | 81 | Distinct canonical regression case. |
| `tests/test_network_negative.py` | `test_network_domain_missing_target` | 81 | Distinct canonical regression case. |
| `tests/test_network_negative.py` | `test_network_class_get_ip_requires_domain` | 78 | Distinct canonical regression case. |
| `tests/test_network_negative.py` | `test_network_call_requires_target` | 78 | Distinct canonical regression case. |
| `tests/test_network_negative.py` | `test_network_instance_domain_and_ip_require_target` | 78 | Distinct canonical regression case. |
| `tests/test_obj.py` | `test_cast_to_int` | 79 |  |
| `tests/test_obj.py` | `test_cast_to_float` | 79 |  |
| `tests/test_obj.py` | `test_cast_to_str` | 79 |  |
| `tests/test_obj.py` | `test_cast_to_multiple_types_first_succeeds` | 79 |  |
| `tests/test_obj.py` | `test_cast_to_multiple_types_second_succeeds` | 79 |  |
| `tests/test_obj.py` | `test_cast_to_bool` | 72 |  |
| `tests/test_obj.py` | `test_cast_to_list` | 79 |  |
| `tests/test_obj.py` | `test_obj_instance_helper` | 79 |  |
| `tests/test_obj.py` | `test_cast_to_none_value` | 75 |  |
| `tests/test_obj.py` | `test_cast_to_complex_object` | 72 |  |
| `tests/test_obj.py` | `TestObjInstance::test_obj_instance_init_none` | 55 | Valid narrow contract. Narrow constructor/property state check. |
| `tests/test_obj.py` | `TestObjInstance::test_obj_instance_init_with_value` | 55 | Narrow constructor/property state check. |
| `tests/test_obj.py` | `TestObjInstance::test_obj_instance_cast_to_int` | 79 |  |
| `tests/test_obj.py` | `TestObjInstance::test_obj_instance_cast_to_float` | 79 |  |
| `tests/test_obj.py` | `TestObjInstance::test_obj_instance_cast_multiple_types` | 79 |  |
| `tests/test_obj.py` | `TestObjInstance::test_obj_instance_cast_with_list` | 79 |  |
| `tests/test_obj.py` | `TestObjInstance::test_obj_instance_cast_bool` | 72 |  |
| `tests/test_obj.py` | `TestObjInstance::test_obj_instance_multiple_casts` | 79 |  |
| `tests/test_obj.py` | `TestObjInstance::test_obj_instance_cast_none` | 75 |  |
| `tests/test_obj_integration.py` | — | 1 | No test functions; required matrix placeholder. |
| `tests/test_obj_integration_negative.py` | — | 1 | No test functions; required matrix placeholder. |
| `tests/test_obj_negative.py` | `test_cast_to_multiple_types_all_fail` | 79 | Distinct canonical regression case. |
| `tests/test_obj_negative.py` | `test_cast_to_returns_original_on_all_failures` | 79 | Distinct canonical regression case. |
| `tests/test_obj_negative.py` | `test_cast_to_empty_type_list` | 82 | Distinct canonical regression case. |
| `tests/test_obj_negative.py` | `test_cast_to_invalid_string_to_int` | 82 | Distinct canonical regression case. |
| `tests/test_obj_negative.py` | `test_cast_to_invalid_string_to_float` | 82 | Distinct canonical regression case. |
| `tests/test_obj_negative.py` | `TestObjInstance::test_obj_instance_cast_fails_returns_original` | 79 | Distinct canonical regression case. |
| `tests/test_obj_negative.py` | `TestObjInstance::test_obj_instance_cast_empty_list` | 82 | Distinct canonical regression case. |
| `tests/test_os.py` | `test_os_python_version_major` | 60 | Valid exact-value or state-transition contract. |
| `tests/test_os.py` | `test_os_sys_platform` | 60 | Valid exact-value or state-transition contract. |
| `tests/test_os.py` | `test_os_name` | 60 | Valid exact-value or state-transition contract. |
| `tests/test_os.py` | `test_os_platform_flags` | 82 |  |
| `tests/test_os.py` | `test_os_architecture` | 72 |  |
| `tests/test_os.py` | `test_os_env` | 70 | Exercises private implementation detail; refactor-sensitive. |
| `tests/test_os.py` | `test_os_nt_family` | 55 | Valid narrow contract. Only type/presence assertion; behavioral regression coverage is weak. |
| `tests/test_os.py` | `test_os_unix_family` | 55 | Valid narrow contract. Only type/presence assertion; behavioral regression coverage is weak. |
| `tests/test_os.py` | `test_os_hostname` | 79 |  |
| `tests/test_os.py` | `TestOSCoverage::test_windows_version` | 79 | Skipped in current environment; platform/dependency branch not runtime-verified here. |
| `tests/test_os.py` | `TestOSCoverage::test_name_caching` | 79 |  |
| `tests/test_os.py` | `TestOSCoverage::test_python_implementation` | 72 |  |
| `tests/test_os.py` | `TestOSCoverage::test_display_property` | 55 | Narrow constructor/property state check. |
| `tests/test_os.py` | `TestOSCoverage::test_running_in_repl` | 79 |  |
| `tests/test_os.py` | `TestOSCoverage::test_cyrillic_support` | 55 | Valid narrow contract. Only type/presence assertion; behavioral regression coverage is weak. |
| `tests/test_os.py` | `TestOSPlatformDetection::test_name_property` | 55 | Valid narrow contract. Narrow constructor/property state check. |
| `tests/test_os.py` | `TestOSPlatformDetection::test_sys_platform_property` | 55 | Valid narrow contract. Narrow constructor/property state check. |
| `tests/test_os.py` | `TestOSPlatformDetection::test_linux_property` | 55 | Valid narrow contract. Narrow constructor/property state check. |
| `tests/test_os.py` | `TestOSPlatformDetection::test_macos_property` | 55 | Valid narrow contract. Narrow constructor/property state check. |
| `tests/test_os.py` | `TestOSPlatformDetection::test_windows_property` | 55 | Valid narrow contract. Narrow constructor/property state check. |
| `tests/test_os.py` | `TestOSSystem::test_system_verbose_true` | 66 | Mock-heavy interaction check; limited real implementation coverage. |
| `tests/test_os.py` | `TestOSSystem::test_system_verbose_false` | 66 | Mock-heavy interaction check; limited real implementation coverage. |
| `tests/test_os.py` | `TestOSProperties::test_args_property` | 55 | Valid narrow contract. Narrow constructor/property state check. |
| `tests/test_os.py` | `TestOSProperties::test_where_method` | 72 |  |
| `tests/test_os.py` | `TestOSProperties::test_env_property` | 55 | Narrow constructor/property state check. |
| `tests/test_os.py` | `TestOSCyrillicSupport::test_cyrillic_support` | 55 | Valid narrow contract. Only type/presence assertion; behavioral regression coverage is weak. |
| `tests/test_os.py` | `TestOSWindowsVersion::test_windows_version_on_windows` | 79 | Skipped in current environment; platform/dependency branch not runtime-verified here. |
| `tests/test_os.py` | `TestOSHostname::test_hostname_property` | 55 | Narrow constructor/property state check. |
| `tests/test_os.py` | `TestOSMultipleCalls::test_cwd_property` | 55 | Narrow constructor/property state check. |
| `tests/test_os.py` | `TestOSMultipleCalls::test_architecture_property` | 55 | Valid narrow contract. Narrow constructor/property state check. |
| `tests/test_os.py` | `TestOSExit::test_exit_method` | 66 | Re-scored after removing shadowing/stale-suite interference. |
| `tests/test_os.py` | `TestOSExit::test_exit_method_with_error_code` | 66 | Re-scored after removing shadowing/stale-suite interference. |
| `tests/test_os.py` | `TestOSDisplayProperty::test_display_property_import_error` | 55 | Valid narrow contract. Exercises private implementation detail; refactor-sensitive. Narrow constructor/property state check. |
| `tests/test_os.py` | `TestOSRunningInRepl::test_running_in_repl_true` | 55 | Valid narrow contract. Exercises private implementation detail; refactor-sensitive. |
| `tests/test_os.py` | `test_os_name_windows_macos_unknown` | 76 |  |
| `tests/test_os.py` | `test_os_display_importerror_sets_false` | 69 |  |
| `tests/test_os.py` | `test_os_python_implementation_pypy_branch` | 73 |  |
| `tests/test_os.py` | `test_os_cyrillic_support_win_unicode_console_enable_success` | 69 |  |
| `tests/test_os.py` | `test_os_cyrillic_support_win_unicode_console_enable_exception` | 69 |  |
| `tests/test_os.py` | `test_os_windows_version_populates_cache` | 73 |  |
| `tests/test_os_integration.py` | `test_os_callable_returns_cwd` | 73 | Distinct canonical regression case. |
| `tests/test_os_integration.py` | `test_os_chdir_updates_cache` | 84 | Distinct canonical regression case. |
| `tests/test_os_integration.py` | `TestOSCoverage::test_walk_basic` | 87 | Distinct canonical regression case. |
| `tests/test_os_integration.py` | `TestOSCoverage::test_walk_topdown_false` | 84 | Distinct canonical regression case. |
| `tests/test_os_integration.py` | `TestOSCoverage::test_walk_follow_links` | 84 | Distinct canonical regression case. |
| `tests/test_os_integration.py` | `TestOSCoverage::test_walk_onerror` | 55 | Valid narrow contract. Only type/presence assertion; behavioral regression coverage is weak. |
| `tests/test_os_integration.py` | `TestOSWalk::test_walk_existing_directory` | 84 | Distinct canonical regression case. |
| `tests/test_os_integration.py` | `TestOSChdirMethod::test_chdir_updates_cwd` | 70 | Exercises private implementation detail; refactor-sensitive. |
| `tests/test_os_integration_negative.py` | `TestOSWalk::test_walk_nonexistent_directory` | 81 | Distinct canonical regression case. |
| `tests/test_os_negative.py` | `TestOSWindowsVersion::test_windows_version_on_non_windows` | 78 | Re-scored after removing shadowing/stale-suite interference. |
| `tests/test_os_negative.py` | `test_os_cyrillic_support_unicode_encode_error_path` | 69 | Distinct canonical regression case. |
| `tests/test_os_negative.py` | `test_os_windows_version_missing_getwindowsversion` | 75 |  |
| `tests/test_path.py` | `TestPathFull::test_full_relative_path` | 79 |  |
| `tests/test_path.py` | `TestPathFull::test_full_already_absolute` | 79 |  |
| `tests/test_path.py` | `TestPathGetRealPath::test_get_real_path` | 72 |  |
| `tests/test_path.py` | `TestPathCommands::test_commands_returns_path` | 75 |  |
| `tests/test_path.py` | `TestPathWorking::test_working_returns_cwd` | 79 |  |
| `tests/test_path.py` | `TestPathCombine::test_combine_basic` | 79 |  |
| `tests/test_path.py` | `TestPathCombine::test_combine_single_path` | 79 |  |
| `tests/test_path.py` | `TestPathInstanceUsage::test_path_string_property` | 79 |  |
| `tests/test_path.py` | `TestPathInstanceUsage::test_path_div_operator` | 79 |  |
| `tests/test_path.py` | `TestPathGetParent::test_get_parent_basic` | 79 |  |
| `tests/test_path.py` | `TestPathGetParent::test_get_parent_windows_style` | 79 |  |
| `tests/test_path.py` | `TestPathGetParent::test_get_parent_no_parent` | 79 |  |
| `tests/test_path.py` | `TestPathAddBeforeExtension::test_add_before_extension_basic` | 79 |  |
| `tests/test_path.py` | `TestPathAddBeforeExtension::test_add_before_extension_multiple_dots` | 79 |  |
| `tests/test_path.py` | `TestPathAddBeforeExtension::test_add_before_extension_no_extension` | 72 |  |
| `tests/test_path.py` | `TestPathPython::test_python_returns_executable` | 75 |  |
| `tests/test_path.py` | `TestPathTemp::test_temp_returns_directory` | 75 |  |
| `tests/test_path.py` | `TestPathSafeFile::test_safe_file` | 72 |  |
| `tests/test_path.py` | `TestPathSeparator::test_separator_returns_os_sep` | 79 |  |
| `tests/test_path.py` | `TestPathSplit::test_split_basic` | 79 |  |
| `tests/test_path.py` | `TestPathSplit::test_split_windows_or_unix` | 79 |  |
| `tests/test_path.py` | `TestPathNegative::test_full_empty_string` | 55 | Valid narrow contract. Only type/presence assertion; behavioral regression coverage is weak. |
| `tests/test_path.py` | `TestPathNegative::test_get_parent_root` | 55 | Valid narrow contract. Only type/presence assertion; behavioral regression coverage is weak. |
| `tests/test_path.py` | `TestPathNegative::test_add_before_extension_empty` | 55 | Valid narrow contract. Only type/presence assertion; behavioral regression coverage is weak. |
| `tests/test_path.py` | `TestPathCombineEdgeCases::test_combine_relative_dot_path` | 75 |  |
| `tests/test_path.py` | `TestPathCombineEdgeCases::test_combine_windows_drive_letter` | 75 |  |
| `tests/test_path.py` | `TestPathCombineEdgeCases::test_combine_smb_path` | 55 | Valid narrow contract. Only type/presence assertion; behavioral regression coverage is weak. |
| `tests/test_path.py` | `TestPathCombineEdgeCases::test_temp_basic` | 82 |  |
| `tests/test_path.py` | `test_path_append_and_string` | 72 |  |
| `tests/test_path.py` | `test_path_truediv` | 72 |  |
| `tests/test_path.py` | `test_path_combine_home` | 73 |  |
| `tests/test_path.py` | `test_path_combine_windows_drive` | 66 |  |
| `tests/test_path.py` | `test_path_home_uses_console` | 73 |  |
| `tests/test_path.py` | `test_path_append_initializes_when_empty` | 78 |  |
| `tests/test_path.py` | `test_path_repr_and_truediv` | 75 |  |
| `tests/test_path.py` | `test_path_combine_windows_smb_and_drive` | 69 |  |
| `tests/test_path.py` | `test_path_home_windows_uses_userprofile` | 66 |  |
| `tests/test_path_integration.py` | `TestPathCombine::test_combine_home_expansion` | 72 | Distinct canonical regression case. |
| `tests/test_path_integration.py` | `TestPathHome::test_home_returns_directory` | 82 | Distinct canonical regression case. |
| `tests/test_path_integration.py` | `TestPathSetWorking::test_set_working` | 79 | Distinct canonical regression case. |
| `tests/test_path_integration.py` | `TestPathCombineEdgeCases::test_set_working_verbose` | 72 | Distinct canonical regression case. |
| `tests/test_path_integration_negative.py` | `TestPathNegative::test_set_working_nonexistent` | 81 | Distinct canonical regression case. |
| `tests/test_path_negative.py` | `TestPathNegative::test_combine_empty_args` | 81 | Distinct canonical regression case. |
| `tests/test_path_negative.py` | `TestPathNegative::test_combine_with_none` | 65 | Verifies deterministic string conversion for a None path shard. |
| `tests/test_print.py` | `test_multithread_safe` | 72 |  |
| `tests/test_print.py` | `test_call_works_as_multithread_safe` | 72 |  |
| `tests/test_print.py` | `test_prettify_dict` | 72 |  |
| `tests/test_print.py` | `test_prettify_list` | 72 |  |
| `tests/test_print.py` | `test_prettify_nested` | 72 |  |
| `tests/test_print.py` | `test_colored_basic` | 72 |  |
| `tests/test_print.py` | `test_colored_with_highlight` | 72 |  |
| `tests/test_print.py` | `test_colored_reverse_order` | 72 |  |
| `tests/test_print.py` | `test_colored_multiple_strings` | 72 |  |
| `tests/test_print.py` | `test_color_output_enabled` | 55 | Valid narrow contract. Only type/presence assertion; behavioral regression coverage is weak. |
| `tests/test_print.py` | `test_prettify_invalid_type` | 55 | Valid narrow contract. Only type/presence assertion; behavioral regression coverage is weak. |
| `tests/test_print.py` | `test_colored_invalid_color` | 75 |  |
| `tests/test_print.py` | `test_print_prefix` | 72 |  |
| `tests/test_print.py` | `test_print_prefix_multiple_args` | 72 |  |
| `tests/test_print.py` | `test_print_prefix_custom_sep` | 72 |  |
| `tests/test_print.py` | `test_debug_basic` | 75 |  |
| `tests/test_print.py` | `test_debug_multiple_strings` | 75 |  |
| `tests/test_print.py` | `test_debug_raw_mode` | 72 |  |
| `tests/test_print.py` | `test_debug_bytes` | 72 |  |
| `tests/test_print.py` | `test_rewrite_basic` | 72 |  |
| `tests/test_print.py` | `test_rewrite_multiple_strings` | 75 |  |
| `tests/test_print.py` | `test_rewrite_custom_sep` | 72 |  |
| `tests/test_print.py` | `test_rewrite_fit_false` | 72 |  |
| `tests/test_print.py` | `test_print_prettify_verbose_prints` | 72 |  |
| `tests/test_print.py` | `test_print_rewrite_windows_trims_width` | 73 | Re-scored after removing shadowing/stale-suite interference. |
| `tests/test_print.py` | `test_print_colored_no_color_env_returns_plain` | 68 | Exercises private implementation detail; refactor-sensitive. |
| `tests/test_print.py` | `test_print_colored_windows_inits_colorama` | 68 | Mock-heavy interaction check; limited real implementation coverage. Exercises private implementation detail; refactor-sensitive. |
| `tests/test_print.py` | `test_print_colored_keyerror_guard` | 68 | Exercises private implementation detail; refactor-sensitive. Re-scored after removing shadowing/stale-suite interference. |
| `tests/test_print_integration.py` | — | 1 | No test functions; required matrix placeholder. |
| `tests/test_print_integration_negative.py` | — | 1 | No test functions; required matrix placeholder. |
| `tests/test_print_negative.py` | `TestPrintMissingCoverage::test_colored_verbose_mode` | 72 | Distinct canonical regression case. |
| `tests/test_process.py` | `test_process9_import` | 50 | Valid public-export smoke test; weak behavioral signal. |
| `tests/test_process.py` | `test_process_instance_helper` | 66 | Mock-heavy interaction check; limited real implementation coverage. |
| `tests/test_process.py` | `test_process_kill_windows_pid` | 73 |  |
| `tests/test_process.py` | `test_process_kill_windows_exe` | 73 |  |
| `tests/test_process.py` | `test_process_kill_unix` | 73 |  |
| `tests/test_process.py` | `test_process_call_sets_target` | 73 |  |
| `tests/test_process.py` | `test_process_call_without_arg_kills_target` | 73 | Mock-heavy interaction check; limited real implementation coverage. |
| `tests/test_process.py` | `test_process_kill_unix_pid_uses_kill` | 73 |  |
| `tests/test_process.py` | `test_process_start_calls_console_get_output` | 76 |  |
| `tests/test_process.py` | `test_process_start_single_arg_sequence` | 73 |  |
| `tests/test_process_integration.py` | — | 1 | No test functions; required matrix placeholder. |
| `tests/test_process_integration_negative.py` | — | 1 | No test functions; required matrix placeholder. |
| `tests/test_process_negative.py` | `test_process_kill_invalid_os` | 75 | Distinct canonical regression case. |
| `tests/test_process_negative.py` | `test_process_kill_target_without_target` | 78 | Distinct canonical regression case. |
| `tests/test_process_negative.py` | `test_process_kill_unsupported_os_raises` | 72 | Distinct canonical regression case. |
| `tests/test_random.py` | `TestRandomInteger::test_integer_basic` | 79 |  |
| `tests/test_random.py` | `TestRandomInteger::test_integer_reversed_range` | 79 |  |
| `tests/test_random.py` | `TestRandomInteger::test_integer_same_min_max` | 79 |  |
| `tests/test_random.py` | `TestRandomInteger::test_integer_to_str` | 79 |  |
| `tests/test_random.py` | `TestRandomInteger::test_integer_negative_range` | 82 |  |
| `tests/test_random.py` | `TestRandomInteger::test_integer_range_includes_endpoints` | 72 |  |
| `tests/test_random.py` | `TestRandomFloat::test_float_basic` | 79 |  |
| `tests/test_random.py` | `TestRandomFloat::test_float_large_range` | 79 |  |
| `tests/test_random.py` | `TestRandomFloat::test_float_negative_range` | 82 |  |
| `tests/test_random.py` | `TestRandomFloat::test_float_different_values` | 79 |  |
| `tests/test_random.py` | `TestRandomString::test_string_basic` | 79 |  |
| `tests/test_random.py` | `TestRandomString::test_string_alphanumeric` | 72 |  |
| `tests/test_random.py` | `TestRandomString::test_string_custom_symbols` | 79 |  |
| `tests/test_random.py` | `TestRandomString::test_string_length_zero` | 79 |  |
| `tests/test_random.py` | `TestRandomString::test_string_different_values` | 79 |  |
| `tests/test_random.py` | `TestRandomItem::test_item_from_list` | 72 |  |
| `tests/test_random.py` | `TestRandomItem::test_item_from_multiple_args` | 72 |  |
| `tests/test_random.py` | `TestRandomItem::test_item_from_dict` | 79 |  |
| `tests/test_random.py` | `TestRandomItem::test_item_from_tuple` | 72 |  |
| `tests/test_random.py` | `TestRandomItem::test_item_kwargs` | 72 |  |
| `tests/test_random.py` | `TestRandomStringUnicode::test_string_unicode_basic` | 82 |  |
| `tests/test_random.py` | `TestRandomStringUnicode::test_string_unicode_contains_unicode` | 75 |  |
| `tests/test_random.py` | `TestRandomStringUnicode::test_string_unicode_different_values` | 82 |  |
| `tests/test_random.py` | `TestRandomBoolean::test_boolean_returns_bool` | 55 | Valid narrow contract. Only type/presence assertion; behavioral regression coverage is weak. |
| `tests/test_random.py` | `TestRandomBoolean::test_boolean_both_values_possible` | 72 |  |
| `tests/test_random.py` | `TestRandomBoolean::test_boolean_approximately_balanced` | 79 |  |
| `tests/test_random.py` | `TestRandomGuid::test_guid_format` | 82 |  |
| `tests/test_random.py` | `TestRandomGuid::test_guid_lowercase` | 79 |  |
| `tests/test_random.py` | `TestRandomGuid::test_guid_hex_chars` | 72 |  |
| `tests/test_random.py` | `TestRandomGuid::test_guid_unique` | 79 |  |
| `tests/test_random.py` | `TestRandomGuid::test_guid_structure` | 82 |  |
| `tests/test_random.py` | `TestRandomShuffle::test_shuffle_string` | 82 |  |
| `tests/test_random.py` | `TestRandomShuffle::test_shuffle_list` | 79 |  |
| `tests/test_random.py` | `TestRandomShuffle::test_shuffle_actually_shuffles` | 72 |  |
| `tests/test_random.py` | `TestRandomShuffle::test_shuffle_preserves_characters` | 79 |  |
| `tests/test_random.py` | `test_random_instance_helpers` | 82 |  |
| `tests/test_random.py` | `test_random_integer_to_str` | 79 |  |
| `tests/test_random.py` | `test_random_shuffle_list_str` | 79 |  |
| `tests/test_random.py` | `TestRandomInstanceComprehensive::test_instance_integer_to_str_branch` | 82 |  |
| `tests/test_random.py` | `TestRandomInstanceComprehensive::test_instance_float_coverage` | 79 |  |
| `tests/test_random.py` | `TestRandomInstanceComprehensive::test_instance_string_with_caching` | 82 |  |
| `tests/test_random.py` | `TestRandomInstanceComprehensive::test_instance_item_single_object` | 72 |  |
| `tests/test_random.py` | `TestRandomInstanceComprehensive::test_instance_item_multiple_args` | 72 |  |
| `tests/test_random.py` | `TestRandomInstanceComprehensive::test_instance_item_kwargs` | 75 |  |
| `tests/test_random.py` | `TestRandomInstanceComprehensive::test_instance_item_dict` | 82 |  |
| `tests/test_random.py` | `TestRandomInstanceComprehensive::test_instance_item_non_dict` | 72 |  |
| `tests/test_random.py` | `TestRandomInstanceComprehensive::test_instance_boolean` | 72 |  |
| `tests/test_random.py` | `TestRandomInstanceComprehensive::test_instance_call_integer_mode` | 79 |  |
| `tests/test_random.py` | `TestRandomInstanceComprehensive::test_instance_call_float_mode` | 79 |  |
| `tests/test_random.py` | `TestClassMethodsComprehensive::test_classmethod_integer_reversed` | 79 |  |
| `tests/test_random.py` | `TestClassMethodsComprehensive::test_classmethod_item_single_list` | 72 |  |
| `tests/test_random.py` | `TestClassMethodsComprehensive::test_classmethod_item_dict` | 72 |  |
| `tests/test_random.py` | `TestClassMethodsComprehensive::test_classmethod_item_kwargs` | 55 | Valid narrow contract. Only type/presence assertion; behavioral regression coverage is weak. |
| `tests/test_random.py` | `TestClassMethodsComprehensive::test_string_unicode_zero_length` | 82 |  |
| `tests/test_random.py` | `TestNegativeCases::test_instance_string_zero_length` | 79 |  |
| `tests/test_random.py` | `TestNegativeCases::test_classmethod_string_zero_length` | 79 |  |
| `tests/test_random.py` | `test_random_class_integer_min_gt_max` | 79 |  |
| `tests/test_random.py` | `test_random_instance_string_symbols_and_item` | 73 |  |
| `tests/test_random.py` | `test_random_unicode_length` | 82 |  |
| `tests/test_random.py` | `test_random_seed_determinism` | 70 | Exercises private implementation detail; refactor-sensitive. |
| `tests/test_random.py` | `TestRandomInstance::test_instance_integer` | 79 |  |
| `tests/test_random.py` | `TestRandomInstance::test_instance_integer_to_str` | 79 |  |
| `tests/test_random.py` | `TestRandomInstance::test_instance_float` | 79 |  |
| `tests/test_random.py` | `TestRandomInstance::test_instance_string` | 79 |  |
| `tests/test_random.py` | `TestRandomInstance::test_instance_string_custom_symbols` | 79 |  |
| `tests/test_random.py` | `TestRandomInstance::test_instance_init_stores_seed` | 70 | Exercises private implementation detail; refactor-sensitive. |
| `tests/test_random.py` | `TestRandomInstance::test_instance_item_list` | 72 |  |
| `tests/test_random.py` | `TestRandomInstance::test_instance_item_multiple_args` | 72 |  |
| `tests/test_random.py` | `TestRandomInstance::test_instance_item_dict` | 72 |  |
| `tests/test_random.py` | `TestRandomInstance::test_instance_item_kwargs` | 72 |  |
| `tests/test_random.py` | `TestRandomInstance::test_instance_boolean` | 72 |  |
| `tests/test_random.py` | `TestRandomInstance::test_instance_call_integer_mode` | 79 |  |
| `tests/test_random.py` | `TestRandomInstance::test_instance_call_float_mode` | 79 |  |
| `tests/test_random.py` | `TestRandomInstance::test_instance_call_default_args` | 79 |  |
| `tests/test_random.py` | `TestRandomInstance::test_instance_call_default_args_float` | 79 |  |
| `tests/test_random.py` | `TestRandomInstance::test_instance_method_shadowing_note` | 55 | Valid narrow contract. Only type/presence assertion; behavioral regression coverage is weak. |
| `tests/test_random.py` | `test_random_instance_integer_to_str_and_call` | 82 |  |
| `tests/test_random.py` | `test_random_instance_float_and_boolean` | 79 |  |
| `tests/test_random.py` | `test_random_instance_string_default_cache` | 72 |  |
| `tests/test_random.py` | `test_random_instance_item_variants` | 75 |  |
| `tests/test_random.py` | `test_random_instance_call_float_mode` | 55 | Valid narrow contract. Only type/presence assertion; behavioral regression coverage is weak. |
| `tests/test_random.py` | `test_random_class_and_instance_overlap` | 76 |  |
| `tests/test_random.py` | `test_random_instance_integer_invalid_range` | 82 |  |
| `tests/test_random_integration.py` | — | 1 | No test functions; required matrix placeholder. |
| `tests/test_random_integration_negative.py` | — | 1 | No test functions; required matrix placeholder. |
| `tests/test_random_negative.py` | `test_random_instance_string_negative_length` | 81 | Distinct canonical regression case. |
| `tests/test_random_negative.py` | `test_random_instance_item_empty` | 75 | Distinct canonical regression case. |
| `tests/test_random_negative.py` | `test_random_class_boolean_and_shuffle_types` | 78 | Distinct canonical regression case. |
| `tests/test_random_negative.py` | `test_random_string_negative_length` | 81 | Distinct canonical regression case. |
| `tests/test_random_negative.py` | `test_random_string_non_int_length` | 78 | Distinct canonical regression case. |
| `tests/test_random_negative.py` | `test_random_item_empty` | 81 | Distinct canonical regression case. |
| `tests/test_random_negative.py` | `test_random_item_invalid_type` | 81 | Distinct canonical regression case. |
| `tests/test_random_negative.py` | `TestRandomInstanceComprehensive::test_instance_string_negative_length` | 81 | Distinct canonical regression case. |
| `tests/test_random_negative.py` | `TestNegativeCases::test_classmethod_string_negative_length` | 81 | Distinct canonical regression case. |
| `tests/test_random_negative.py` | `TestNegativeCases::test_instance_item_empty_list` | 81 | Distinct canonical regression case. |
| `tests/test_random_negative.py` | `TestNegativeCases::test_classmethod_item_empty_list` | 81 | Distinct canonical regression case. |
| `tests/test_random_negative.py` | `test_random_class_string_negative` | 78 | Re-scored after removing shadowing/stale-suite interference. |
| `tests/test_random_negative.py` | `TestRandomInstance::test_instance_string_negative_length` | 81 | Distinct canonical regression case. |
| `tests/test_random_negative.py` | `test_random_class_item_empty_raises` | 81 | Distinct canonical regression case. |
| `tests/test_random_negative.py` | `test_random_class_shuffle_non_iterable` | 78 |  |
| `tests/test_screen.py` | `test_screen9_import` | 50 | Valid public-export smoke test; weak behavioral signal. |
| `tests/test_screen.py` | `test_screen_instance_helper` | 73 |  |
| `tests/test_screen.py` | `TestScreenCoverage::test_get_pixel_color_without_stub` | 73 |  |
| `tests/test_screen_integration.py` | — | 1 | No test functions; required matrix placeholder. |
| `tests/test_screen_integration_negative.py` | — | 1 | No test functions; required matrix placeholder. |
| `tests/test_screen_negative.py` | `TestScreenCoverage::test_color_instance_without_position_raises` | 78 | Distinct canonical regression case. |
| `tests/test_ssh.py` | `test_ssh9_import` | 50 | Valid public-export smoke test; weak behavioral signal. |
| `tests/test_ssh.py` | `TestSshCoverage::test_credentials_success` | 70 | Exercises private implementation detail; refactor-sensitive. |
| `tests/test_ssh.py` | `TestSshCoverage::test_command_with_safe_none_uses_instance_safe` | 76 |  |
| `tests/test_ssh.py` | `TestSshCoverage::test_avg_load_with_safe_none_uses_instance_safe` | 76 |  |
| `tests/test_ssh.py` | `TestSshCoverage::test_uptime_with_safe_none_uses_instance_safe` | 76 |  |
| `tests/test_ssh.py` | `test_ssh_get_output_success` | 70 | Exercises private implementation detail; refactor-sensitive. |
| `tests/test_ssh.py` | `test_ssh_get_output_safe` | 79 |  |
| `tests/test_ssh.py` | `test_ssh_avg_load_and_uptime` | 73 |  |
| `tests/test_ssh.py` | `test_ssh_import` | 50 | Valid public-export smoke test; weak behavioral signal. |
| `tests/test_ssh_integration.py` | — | 1 | No test functions; required matrix placeholder. |
| `tests/test_ssh_integration_negative.py` | — | 1 | No test functions; required matrix placeholder. |
| `tests/test_ssh_negative.py` | `test_ssh_credentials_missing` | 81 | Distinct canonical regression case. |
| `tests/test_ssh_negative.py` | `test_ssh_avg_load_missing_credentials` | 81 | Distinct canonical regression case. |
| `tests/test_ssh_negative.py` | `test_ssh_uptime_missing_credentials` | 81 | Distinct canonical regression case. |
| `tests/test_ssh_negative.py` | `test_ssh_get_output_raises_on_pypy` | 72 | Distinct canonical regression case. |
| `tests/test_str.py` | `TestStrQuotes::test_to_quotes` | 82 |  |
| `tests/test_str.py` | `TestStrQuotes::test_to_quotes_2` | 82 |  |
| `tests/test_str.py` | `TestStrGetIntegers::test_get_integers_basic` | 82 |  |
| `tests/test_str.py` | `TestStrGetIntegers::test_get_integers_negative` | 85 |  |
| `tests/test_str.py` | `TestStrGetIntegers::test_get_integers_floats` | 82 |  |
| `tests/test_str.py` | `TestStrGetIntegers::test_get_integers_no_float_support` | 72 |  |
| `tests/test_str.py` | `TestStrGetIntegers::test_get_integers_mixed` | 79 |  |
| `tests/test_str.py` | `TestStrNewlines::test_newlines_to_strings` | 79 |  |
| `tests/test_str.py` | `TestStrNewlines::test_newlines_to_strings_crlf` | 79 |  |
| `tests/test_str.py` | `TestStrNewlines::test_newlines_to_strings_empty` | 82 |  |
| `tests/test_str.py` | `TestStrNewlines::test_nl_alias` | 79 |  |
| `tests/test_str.py` | `TestStrSplitEvery::test_split_every_basic` | 79 |  |
| `tests/test_str.py` | `TestStrSplitEvery::test_split_every_uneven` | 79 |  |
| `tests/test_str.py` | `TestStrSplitEvery::test_split_every_reverse` | 79 |  |
| `tests/test_str.py` | `TestStrSplitEvery::test_split_every_integers` | 79 |  |
| `tests/test_str.py` | `TestStrPadding::test_leftpad_basic` | 79 |  |
| `tests/test_str.py` | `TestStrPadding::test_leftpad_custom_char` | 79 |  |
| `tests/test_str.py` | `TestStrPadding::test_leftpad_no_padding_needed` | 79 |  |
| `tests/test_str.py` | `TestStrPadding::test_rightpad_basic` | 79 |  |
| `tests/test_str.py` | `TestStrPadding::test_rightpad_custom_char` | 79 |  |
| `tests/test_str.py` | `TestStrSubstring::test_substring_basic` | 79 |  |
| `tests/test_str.py` | `TestStrSubstring::test_substring_before_only` | 79 |  |
| `tests/test_str.py` | `TestStrSubstring::test_substring_safe_mode` | 79 |  |
| `tests/test_str.py` | `TestStrRemoveSpaces::test_remove_spaces_basic` | 79 |  |
| `tests/test_str.py` | `TestStrRemoveSpaces::test_remove_spaces_single_spaces_unchanged` | 79 |  |
| `tests/test_str.py` | `TestStrGetWords::test_get_words_basic` | 75 |  |
| `tests/test_str.py` | `TestStrRreplace::test_rreplace_basic` | 79 |  |
| `tests/test_str.py` | `TestStrRreplace::test_rreplace_multiple` | 79 |  |
| `tests/test_str.py` | `TestStrIsAscii::test_is_ascii_true` | 72 |  |
| `tests/test_str.py` | `TestStrIsAscii::test_is_ascii_false` | 72 |  |
| `tests/test_str.py` | `TestStrGuidFromSeed::test_guid_from_seed_deterministic` | 79 |  |
| `tests/test_str.py` | `TestStrGuidFromSeed::test_guid_from_seed_different` | 79 |  |
| `tests/test_str.py` | `TestStrNegative::test_to_quotes_none` | 82 |  |
| `tests/test_str.py` | `TestStrNegative::test_get_integers_empty_string` | 82 |  |
| `tests/test_str.py` | `TestStrNegative::test_get_integers_special_chars_only` | 79 |  |
| `tests/test_str.py` | `TestStrNegative::test_get_integers_very_large_number` | 79 |  |
| `tests/test_str.py` | `TestStrNegative::test_newlines_to_strings_mixed_newlines` | 72 |  |
| `tests/test_str.py` | `TestStrNegative::test_split_every_empty_string` | 82 |  |
| `tests/test_str.py` | `TestStrNegative::test_split_every_very_large_chars` | 79 |  |
| `tests/test_str.py` | `TestStrNegative::test_leftpad_negative_length` | 55 | Valid narrow contract. Only type/presence assertion; behavioral regression coverage is weak. |
| `tests/test_str.py` | `TestStrNegative::test_rightpad_zero_length` | 55 | Valid narrow contract. Only type/presence assertion; behavioral regression coverage is weak. |
| `tests/test_str.py` | `TestStrNegative::test_substring_both_markers_missing` | 55 | Valid narrow contract. Only type/presence assertion; behavioral regression coverage is weak. |
| `tests/test_str.py` | `TestStrNegative::test_remove_spaces_empty_string` | 82 |  |
| `tests/test_str.py` | `TestStrNegative::test_remove_spaces_only_spaces` | 79 |  |
| `tests/test_str.py` | `TestStrNegative::test_get_words_empty_string` | 55 | Valid narrow contract. Only type/presence assertion; behavioral regression coverage is weak. |
| `tests/test_str.py` | `TestStrNegative::test_rreplace_count_zero` | 79 |  |
| `tests/test_str.py` | `TestStrNegative::test_rreplace_not_found` | 79 |  |
| `tests/test_str.py` | `TestStrNegative::test_is_ascii_empty_string` | 75 |  |
| `tests/test_str.py` | `TestStrNegative::test_guid_from_seed_empty` | 82 |  |
| `tests/test_str.py` | `TestStrCoverage::test_get_integers_with_debug` | 79 |  |
| `tests/test_str.py` | `TestStrCoverage::test_get_integers_multiple_decimal_points` | 72 |  |
| `tests/test_str.py` | `TestStrCoverage::test_substring_with_bytes_string` | 79 |  |
| `tests/test_str.py` | `TestStrCoverage::test_substring_with_bytes_before` | 79 |  |
| `tests/test_str.py` | `TestStrCoverage::test_substring_with_bytes_after` | 55 | Valid narrow contract. Only type/presence assertion; behavioral regression coverage is weak. |
| `tests/test_str.py` | `TestStrCoverage::test_substring_non_string_conversions` | 79 |  |
| `tests/test_str.py` | `TestStrCoverage::test_substring_bytes_after_duplicate_check` | 72 |  |
| `tests/test_str.py` | `TestStrCoverage::test_substring_return_after_substring_found` | 79 |  |
| `tests/test_str.py` | `TestStrCoverage::test_substring_return_after_substring_not_found` | 79 |  |
| `tests/test_str.py` | `TestStrCoverage::test_substring_return_after_tuple` | 79 |  |
| `tests/test_str.py` | `TestStrCoverage::test_diff_simple` | 72 |  |
| `tests/test_str.py` | `TestStrCoverage::test_input_pass_mocked` | 73 |  |
| `tests/test_str.py` | `TestStrCoverage::test_encrypt_decrypt` | 79 |  |
| `tests/test_str.py` | `TestStrCoverage::test_decrypt_invalid_chr_values` | 82 |  |
| `tests/test_str.py` | `TestStrCoverage::test_guid_by_seed_basic` | 79 |  |
| `tests/test_str.py` | `TestStrCoverage::test_guid_by_seed_allow_duplicate` | 79 |  |
| `tests/test_str.py` | `TestStrCoverage::test_rreplace_with_non_string_types` | 79 |  |
| `tests/test_str.py` | `test_str_instance_helpers` | 82 |  |
| `tests/test_str.py` | `test_str_substring_after_bytes_is_converted` | 79 |  |
| `tests/test_str.py` | `TestStrInstanceMethodsShadowed::test_instance_to_quotes_direct` | 79 |  |
| `tests/test_str.py` | `TestStrInstanceMethodsShadowed::test_instance_to_quotes_2_direct` | 79 |  |
| `tests/test_str.py` | `TestStrInstanceMethodsShadowed::test_instance_split_every_direct` | 79 |  |
| `tests/test_str.py` | `TestStrInstanceMethodsShadowed::test_instance_leftpad_direct` | 79 |  |
| `tests/test_str.py` | `TestStrInstanceMethodsShadowed::test_instance_rightpad_direct` | 79 |  |
| `tests/test_str.py` | `TestStrSubstringEdgeCases::test_substring_after_is_bytes_duplicate_check` | 79 |  |
| `tests/test_str.py` | `TestStrSubstringEdgeCases::test_substring_after_conversion_in_after_block` | 79 |  |
| `tests/test_str.py` | `TestStrInputIntMethod::test_input_int_with_default_enter` | 73 | Mock-heavy interaction check; limited real implementation coverage. |
| `tests/test_str.py` | `TestStrInputIntMethod::test_input_int_valid_input` | 73 |  |
| `tests/test_str.py` | `TestStrInputIntMethod::test_input_int_non_integer_then_valid` | 73 |  |
| `tests/test_str.py` | `TestStrInputIntMethod::test_input_int_no_debug` | 73 |  |
| `tests/test_str.py` | `TestStrEncryptDecrypt::test_decrypt_chr_overflow` | 82 |  |
| `tests/test_str.py` | `TestStrRReplace::test_rreplace_non_int_occurrence` | 79 |  |
| `tests/test_str.py` | `TestStrRReplace::test_rreplace_with_int_occurrence` | 79 |  |
| `tests/test_str.py` | `TestStrRReplace::test_rreplace_multiple_occurrences` | 79 |  |
| `tests/test_str.py` | `TestStrAdditionalEdgeCases::test_substring_bytes_before` | 79 |  |
| `tests/test_str.py` | `TestStrAdditionalEdgeCases::test_substring_bytes_after` | 79 |  |
| `tests/test_str.py` | `TestStrAdditionalEdgeCases::test_decrypt_chr_negative` | 82 |  |
| `tests/test_str.py` | `TestStrGuidBySeed::test_guid_by_seed_basic` | 79 |  |
| `tests/test_str.py` | `TestStrGuidBySeed::test_guid_by_seed_allow_duplicate` | 55 | Valid narrow contract. Only type/presence assertion; behavioral regression coverage is weak. |
| `tests/test_str.py` | `TestStrInstanceMethods::test_instance_to_quotes` | 79 |  |
| `tests/test_str.py` | `TestStrInstanceMethods::test_instance_to_quotes_2` | 79 |  |
| `tests/test_str.py` | `TestStrInstanceMethods::test_instance_split_every` | 79 |  |
| `tests/test_str.py` | `TestStrInstanceMethods::test_instance_leftpad` | 79 |  |
| `tests/test_str.py` | `TestStrInstanceMethods::test_instance_leftpad_custom_char` | 79 |  |
| `tests/test_str.py` | `TestStrInstanceMethods::test_instance_rightpad` | 79 |  |
| `tests/test_str.py` | `TestStrInstanceMethods::test_instance_rightpad_custom_char` | 79 |  |
| `tests/test_str.py` | `TestStrInstanceMethods::test_substring_with_bytes_after_parameter` | 79 |  |
| `tests/test_str.py` | `TestStrMissingCoverage::test_instance_to_quotes` | 79 |  |
| `tests/test_str.py` | `TestStrMissingCoverage::test_instance_to_quotes_2` | 79 |  |
| `tests/test_str.py` | `TestStrMissingCoverage::test_instance_split_every` | 79 |  |
| `tests/test_str.py` | `TestStrMissingCoverage::test_instance_split_every_reverse` | 79 |  |
| `tests/test_str.py` | `TestStrMissingCoverage::test_instance_leftpad` | 79 |  |
| `tests/test_str.py` | `TestStrMissingCoverage::test_instance_leftpad_with_char` | 79 |  |
| `tests/test_str.py` | `TestStrMissingCoverage::test_instance_leftpad_rightpad_mode` | 79 |  |
| `tests/test_str.py` | `TestStrMissingCoverage::test_instance_rightpad` | 79 |  |
| `tests/test_str.py` | `TestStrMissingCoverage::test_instance_rightpad_with_char` | 79 |  |
| `tests/test_str_integration.py` | — | 1 | No test functions; required matrix placeholder. |
| `tests/test_str_integration_negative.py` | — | 1 | No test functions; required matrix placeholder. |
| `tests/test_str_negative.py` | `TestStrNewlines::test_newlines_to_strings_invalid_type` | 81 | Distinct canonical regression case. |
| `tests/test_str_negative.py` | `TestStrSplitEvery::test_split_every_invalid_chars` | 81 | Distinct canonical regression case. |
| `tests/test_str_negative.py` | `TestStrSplitEvery::test_split_every_unsupported_type` | 78 | Distinct canonical regression case. |
| `tests/test_str_negative.py` | `TestStrSubstring::test_substring_not_found` | 78 | Distinct canonical regression case. |
| `tests/test_str_negative.py` | `TestStrSubstring::test_substring_custom_exception_message` | 78 | Distinct canonical regression case. |
| `tests/test_str_negative.py` | `TestStrCoverage::test_substring_after_not_found_exception` | 78 | Distinct canonical regression case. |
| `tests/test_str_negative.py` | `TestStrCoverage::test_guid_by_seed_duplicate_raises` | 78 | Distinct canonical regression case. |
| `tests/test_str_negative.py` | `TestStrSubstringEdgeCases::test_substring_after_not_found_with_exception_message` | 78 | Distinct canonical regression case. |
| `tests/test_str_negative.py` | `TestStrInputIntMethod::test_input_int_empty_no_default` | 75 | Distinct canonical regression case. |
| `tests/test_str_negative.py` | `TestStrInputIntMethod::test_input_int_with_minimum_invalid` | 75 | Distinct canonical regression case. |
| `tests/test_str_negative.py` | `TestStrInputIntMethod::test_input_int_with_maximum_invalid` | 75 | Distinct canonical regression case. |
| `tests/test_str_negative.py` | `TestStrGuidBySeed::test_guid_by_seed_duplicate_error` | 81 | Distinct canonical regression case. |
| `tests/test_threading.py` | `test_mythread_callable_runs` | 66 |  |
| `tests/test_threading.py` | `test_mythread_kill_sets_flag` | 72 |  |
| `tests/test_threading.py` | `test_threading_callable_starts` | 73 |  |
| `tests/test_threading.py` | `test_threading_add_defaults` | 79 |  |
| `tests/test_threading.py` | `TestMyThreadComprehensive::test_qprint_verbose_true` | 66 | Mock-heavy interaction check; limited real implementation coverage. |
| `tests/test_threading.py` | `TestMyThreadComprehensive::test_qprint_verbose_false` | 66 | Mock-heavy interaction check; limited real implementation coverage. |
| `tests/test_threading.py` | `TestMyThreadComprehensive::test_start_verbose_true` | 72 | Re-scored after removing shadowing/stale-suite interference. |
| `tests/test_threading.py` | `TestMyThreadComprehensive::test_is_running` | 72 | Re-scored after removing shadowing/stale-suite interference. |
| `tests/test_threading.py` | `TestMyThreadComprehensive::test_globaltrace_and_localtrace` | 88 |  |
| `tests/test_threading.py` | `TestThreadingComprehensive::test_runner_verbose_true` | 72 | Re-scored after removing shadowing/stale-suite interference. |
| `tests/test_threading.py` | `TestThreadingComprehensive::test_start_max_threads_zero` | 74 | Wall-clock dependence adds timing-flake risk. |
| `tests/test_threading.py` | `TestThreadingComprehensive::test_get_ids` | 79 | Re-scored after removing shadowing/stale-suite interference. |
| `tests/test_threading.py` | `TestThreadingComprehensive::test_raise_exception` | 67 | Wall-clock dependence adds timing-flake risk. |
| `tests/test_threading.py` | `TestThreadingComprehensive::test_get_results` | 79 |  |
| `tests/test_threading.py` | `TestThreadingComprehensive::test_is_running` | 68 | Wall-clock dependence adds timing-flake risk. |
| `tests/test_threading.py` | `TestThreadingComprehensive::test_running_threads` | 79 | Re-scored after removing shadowing/stale-suite interference. |
| `tests/test_threading.py` | `TestThreadingCallable::test_threading_call` | 72 |  |
| `tests/test_threading.py` | `TestMyThreadCallable::test_mythread_call` | 72 |  |
| `tests/test_threading.py` | `TestThreadingStartFromFirst::test_start_from_first_true` | 79 | Re-scored after removing shadowing/stale-suite interference. |
| `tests/test_threading.py` | `test_threading_runner_flow` | 73 |  |
| `tests/test_threading.py` | `test_mythread_run_restores_trace_and_sets_result` | 73 | Mock-heavy interaction check; limited real implementation coverage. |
| `tests/test_threading.py` | `test_mythread_run_chains_existing_trace_and_restores_it` | 70 | Exercises private implementation detail; refactor-sensitive. |
| `tests/test_threading.py` | `test_threading_runner_executes_tasks_in_main_thread` | 76 |  |
| `tests/test_threading.py` | `test_threading_wait_keyboard_interrupt` | 73 |  |
| `tests/test_threading.py` | `test_threading_cleanup_resets` | 76 |  |
| `tests/test_threading_integration.py` | `TestThreadingIntegration::test_threading_with_cleanup` | 79 |  |
| `tests/test_threading_integration.py` | `TestThreadingIntegration::test_threading_get_results_integration` | 74 | Wall-clock dependence adds timing-flake risk. |
| `tests/test_threading_integration.py` | `TestThreadingIntegration::test_threading_is_running_integration` | 74 | Wall-clock dependence adds timing-flake risk. |
| `tests/test_threading_integration.py` | `TestThreadingIntegration::test_threading_running_threads_integration` | 74 | Wall-clock dependence adds timing-flake risk. |
| `tests/test_threading_integration.py` | `TestThreadingIntegration::test_threading_total_input_threads` | 79 |  |
| `tests/test_threading_integration.py` | `TestThreadingIntegration::test_threading_start_from_first` | 74 | Wall-clock dependence adds timing-flake risk. |
| `tests/test_threading_integration.py` | `TestThreadingIntegration::test_mythread_kill` | 67 | Wall-clock dependence adds timing-flake risk. |
| `tests/test_threading_integration.py` | `TestThreadingIntegration::test_threading_kill` | 67 | Wall-clock dependence adds timing-flake risk. |
| `tests/test_threading_integration.py` | `TestThreadingIntegration::test_threading_wait_for_completion` | 74 | Wall-clock dependence adds timing-flake risk. |
| `tests/test_threading_integration.py` | `TestThreadingIntegration::test_mythread_callable` | 72 |  |
| `tests/test_threading_integration.py` | `TestThreadingIntegration::test_threading_callable` | 72 |  |
| `tests/test_threading_integration_negative.py` | — | 1 | No test functions; required matrix placeholder. |
| `tests/test_threading_negative.py` | `TestThreadingMissingCoverage::test_mythread_verbose_mode` | 79 | Distinct canonical regression case. |
| `tests/test_threading_negative.py` | `TestThreadingMissingCoverage::test_mythread_wait_for_keyboard_interrupt` | 79 | Distinct canonical regression case. |
| `tests/test_threading_negative.py` | `TestThreadingMissingCoverage::test_mythread_is_running` | 67 | Wall-clock dependence adds timing-flake risk. |
| `tests/test_threading_negative.py` | `TestThreadingMissingCoverage::test_threading_with_verbose` | 74 | Wall-clock dependence adds timing-flake risk. |
| `tests/test_threading_negative.py` | `TestThreadingMissingCoverage::test_threading_max_threads_zero` | 74 | Wall-clock dependence adds timing-flake risk. |
| `tests/test_threading_negative.py` | `TestThreadingMissingCoverage::test_threading_start_from_first` | 74 | Wall-clock dependence adds timing-flake risk. |
| `tests/test_threading_negative.py` | `TestThreadingMissingCoverage::test_threading_wait_for_keyboard_interrupt` | 74 | Wall-clock dependence adds timing-flake risk. |
| `tests/test_threading_negative.py` | `TestThreadingMissingCoverage::test_threading_cleanup` | 82 | Distinct canonical regression case. |
| `tests/test_threading_negative.py` | `TestThreadingMissingCoverage::test_threading_get_ids` | 79 | Re-scored after removing shadowing/stale-suite interference. |
| `tests/test_threading_negative.py` | `TestThreadingMissingCoverage::test_threading_raise_exception` | 79 | Re-scored after removing shadowing/stale-suite interference. |
| `tests/test_threading_negative.py` | `TestThreadingMissingCoverage::test_threading_get_results` | 74 | Wall-clock dependence adds timing-flake risk. |
| `tests/test_threading_negative.py` | `TestThreadingMissingCoverage::test_threading_is_running` | 79 | Distinct canonical regression case. |
| `tests/test_threading_negative.py` | `TestThreadingMissingCoverage::test_threading_running_threads` | 74 | Wall-clock dependence adds timing-flake risk. |
| `tests/test_threading_negative.py` | `TestMyThreadComprehensive::test_run_system_exit` | 66 | Mock-heavy interaction check; limited real implementation coverage. |
| `tests/test_threading_negative.py` | `TestMyThreadComprehensive::test_wait_for_keyboard_interrupt_with_exception` | 73 | Wall-clock dependence adds timing-flake risk. |
| `tests/test_threading_negative.py` | `TestThreadingComprehensive::test_wait_for_keyboard_interrupt_with_exception` | 78 | Distinct canonical regression case. |
| `tests/test_threading_negative.py` | `test_threading_start_no_threads` | 78 | Distinct canonical regression case. |
| `tests/test_threading_negative.py` | `test_mythread_localtrace_and_kill` | 78 | Distinct canonical regression case. |
| `tests/test_threading_negative.py` | `test_mythread_kill_triggers_system_exit_on_trace_call` | 78 |  |
| `tests/test_threading_negative.py` | `test_mythread_wait_for_keyboard_interrupt_kills_and_reraises` | 72 |  |
| `tests/test_threading_negative.py` | `test_threading_wait_for_keyboard_interrupt_kills_all` | 75 |  |
| `tests/test_time.py` | `TestTimeStamp::test_stamp_returns_float` | 55 | Valid narrow contract. Only type/presence assertion; behavioral regression coverage is weak. |
| `tests/test_time.py` | `TestTimeStamp::test_stamp_is_current` | 74 | Wall-clock dependence adds timing-flake risk. |
| `tests/test_time.py` | `TestTimeDatetime::test_datetime_no_args` | 55 | Valid narrow contract. Only type/presence assertion; behavioral regression coverage is weak. |
| `tests/test_time.py` | `TestTimeDatetime::test_datetime_with_year` | 79 |  |
| `tests/test_time.py` | `TestTimeDatetime::test_datetime_with_multiple_args` | 82 |  |
| `tests/test_time.py` | `TestTimeDatetime::test_datetime_with_time` | 82 |  |
| `tests/test_time.py` | `TestTimeTimestampToDatetime::test_timestamp_to_datetime_float` | 74 | Wall-clock dependence adds timing-flake risk. |
| `tests/test_time.py` | `TestTimeTimestampToDatetime::test_timestamp_to_datetime_int` | 55 | Valid narrow contract. Wall-clock dependence adds timing-flake risk. |
| `tests/test_time.py` | `TestTimeTimestampToDatetime::test_timestamp_to_datetime_string` | 55 | Valid narrow contract. Wall-clock dependence adds timing-flake risk. |
| `tests/test_time.py` | `TestTimeTimestampToDatetime::test_timestamp_to_datetime_already_datetime` | 74 | Wall-clock dependence adds timing-flake risk. |
| `tests/test_time.py` | `TestTimeDatetimeToTimestamp::test_datetime_to_timestamp` | 55 | Valid narrow contract. Only type/presence assertion; behavioral regression coverage is weak. |
| `tests/test_time.py` | `TestTimeDatetimeToTimestamp::test_datetime_to_timestamp_already_float` | 79 |  |
| `tests/test_time.py` | `TestTimeDatetimeToTimestamp::test_datetime_to_timestamp_roundtrip` | 74 | Wall-clock dependence adds timing-flake risk. |
| `tests/test_time.py` | `TestTimeDotted::test_dotted_current_time` | 82 |  |
| `tests/test_time.py` | `TestTimeDotted::test_dotted_custom_timestamp` | 72 |  |
| `tests/test_time.py` | `TestTimeDotted::test_dotted_custom_datetime` | 72 |  |
| `tests/test_time.py` | `TestTimeSleep::test_sleep_basic` | 74 | Wall-clock dependence adds timing-flake risk. |
| `tests/test_time.py` | `TestTimeSleep::test_sleep_zero` | 73 | Re-scored after removing shadowing/stale-suite interference. |
| `tests/test_time.py` | `TestTimeDelta::test_delta_single_arg` | 74 | Wall-clock dependence adds timing-flake risk. |
| `tests/test_time.py` | `TestTimeDelta::test_delta_two_timestamps` | 79 |  |
| `tests/test_time.py` | `TestTimeDelta::test_delta_reversed_order` | 79 |  |
| `tests/test_time.py` | `TestTimeDelta::test_delta_datetime_objects` | 79 |  |
| `tests/test_time.py` | `TestTimeHumanReadable::test_human_readable_seconds` | 72 |  |
| `tests/test_time.py` | `TestTimeHumanReadable::test_human_readable_minutes` | 72 |  |
| `tests/test_time.py` | `TestTimeHumanReadable::test_human_readable_hours` | 72 |  |
| `tests/test_time.py` | `TestTimeHumanReadable::test_human_readable_days` | 72 |  |
| `tests/test_time.py` | `TestTimeHumanReadable::test_human_readable_timedelta` | 67 | Wall-clock dependence adds timing-flake risk. |
| `tests/test_time.py` | `TestTimeHumanReadable::test_human_readable_microseconds` | 72 |  |
| `tests/test_time.py` | `TestTimeCoverage::test_datetime_with_microsecond` | 79 |  |
| `tests/test_time.py` | `TestTimeCoverage::test_datetime_with_tzinfo` | 74 | Wall-clock dependence adds timing-flake risk. |
| `tests/test_time.py` | `TestTimeCoverage::test_datetime_with_fold` | 79 |  |
| `tests/test_time.py` | `TestTimeCoverage::test_sleep_verbose` | 74 | Wall-clock dependence adds timing-flake risk. |
| `tests/test_time.py` | `TestTimeCoverage::test_sleep_verbose_longer` | 74 | Wall-clock dependence adds timing-flake risk. |
| `tests/test_time.py` | `test_time_instance_helpers` | 74 | Wall-clock dependence adds timing-flake risk. |
| `tests/test_time.py` | `test_time_timer_fast_seconds_gt_1` | 63 | Exercises private implementation detail; refactor-sensitive. Wall-clock dependence adds timing-flake risk. |
| `tests/test_time.py` | `test_time_timer_fast_seconds_le_1` | 63 | Exercises private implementation detail; refactor-sensitive. Wall-clock dependence adds timing-flake risk. |
| `tests/test_time.py` | `test_time_instance_delta_no_args_uses_same_datetime` | 79 |  |
| `tests/test_time.py` | `test_time_callable_delta` | 55 | Valid narrow contract. Wall-clock dependence adds timing-flake risk. |
| `tests/test_time.py` | `test_time_callable_timestamp` | 55 | Valid narrow contract. Wall-clock dependence adds timing-flake risk. |
| `tests/test_time_integration.py` | — | 1 | No test functions; required matrix placeholder. |
| `tests/test_time_integration_negative.py` | — | 1 | No test functions; required matrix placeholder. |
| `tests/test_time_negative.py` | `TestTimeTimestampToDatetime::test_timestamp_to_datetime_invalid_type` | 76 | Wall-clock dependence adds timing-flake risk. |
| `tests/test_time_negative.py` | `TestTimeSleep::test_sleep_negative_raises` | 76 | Wall-clock dependence adds timing-flake risk. |
| `tests/test_time_negative.py` | `test_time_sleep_negative` | 76 | Wall-clock dependence adds timing-flake risk. |
| `tests/test_tkinter.py` | `test_tkinter9_import` | 50 | Valid public-export smoke test; weak behavioral signal. |
| `tests/test_tkinter.py` | `test_tkinter_color_rgb` | 79 |  |
| `tests/test_tkinter.py` | `test_tkinter_color_formats_hex` | 82 |  |
| `tests/test_tkinter.py` | `test_tkinter_instance_rgb_uses_defaults` | 79 |  |
| `tests/test_tkinter.py` | `test_tkinter_instance_rgb_overrides_defaults` | 79 |  |
| `tests/test_tkinter_integration.py` | — | 1 | No test functions; required matrix placeholder. |
| `tests/test_tkinter_integration_negative.py` | — | 1 | No test functions; required matrix placeholder. |
| `tests/test_tkinter_negative.py` | `test_tkinter_rgb_missing` | 81 | Distinct canonical regression case. |
| `tests/test_tkinter_negative.py` | `test_tkinter_instance_rgb_missing_raises` | 81 | Distinct canonical regression case. |
| `tests/test_tsql.py` | `test_tsql9_import` | 50 | Valid public-export smoke test; weak behavioral signal. |
| `tests/test_tsql.py` | `test_tsql_call_delegates_to_run` | 73 |  |
| `tests/test_tsql.py` | `test_tsql_run_debug_success_commits_and_closes` | 76 |  |
| `tests/test_tsql.py` | `test_tsql_run_without_transaction_debug_nextset_loop` | 61 | Exercises private implementation detail; refactor-sensitive. |
| `tests/test_tsql.py` | `test_tsql_query_single_result_returns_flat_list` | 73 |  |
| `tests/test_tsql.py` | `test_tsql_drop_table_force_adds_alter` | 66 |  |
| `tests/test_tsql.py` | `test_tsql_query_success_with_debug` | 70 | Exercises private implementation detail; refactor-sensitive. |
| `tests/test_tsql.py` | `test_tsql_drop_helpers` | 69 |  |
| `tests/test_tsql.py` | `test_tsql_backup_database_paths` | 76 |  |
| `tests/test_tsql.py` | `test_tsql_backup_database_existing_file` | 73 |  |
| `tests/test_tsql.py` | `test_tsql_get_file_sizes_and_space` | 73 |  |
| `tests/test_tsql.py` | `test_tsql_run_without_transaction_success` | 76 | Re-scored after removing shadowing/stale-suite interference. |
| `tests/test_tsql_integration.py` | — | 1 | No test functions; required matrix placeholder. |
| `tests/test_tsql_integration_negative.py` | — | 1 | No test functions; required matrix placeholder. |
| `tests/test_tsql_negative.py` | `test_tsql_run_import_error` | 75 | Distinct canonical regression case. |
| `tests/test_tsql_negative.py` | `test_tsql_run_connection_error` | 75 | Verifies interface errors become the documented programming-error type. |
| `tests/test_tsql_negative.py` | `test_tsql_run_importerror` | 75 | Distinct canonical regression case. |
| `tests/test_tsql_negative.py` | `test_tsql_run_programming_error` | 75 | Distinct canonical regression case. |
| `tests/test_tsql_negative.py` | `test_tsql_run_interface_error_wrapped` | 78 | Distinct canonical regression case. |
| `tests/test_tsql_negative.py` | `test_tsql_run_programming_error_wrapped` | 75 | Distinct canonical regression case. |
| `tests/test_tsql_negative.py` | `test_tsql_run_without_transaction_programming_error_wrapped` | 75 | Distinct canonical regression case. |
| `tests/test_tsql_negative.py` | `test_tsql_query_import_error_prints_message` | 75 | Distinct canonical regression case. |
| `tests/test_tsql_negative.py` | `test_tsql_query_programming_error` | 75 |  |
| `tests/test_tsql_negative.py` | `test_tsql_run_without_transaction_import_error` | 75 |  |
| `tests/test_version.py` | — | 1 | No test functions; required matrix placeholder. |
| `tests/test_version_integration.py` | — | 1 | No test functions; required matrix placeholder. |
| `tests/test_version_integration_negative.py` | — | 1 | No test functions; required matrix placeholder. |
| `tests/test_version_negative.py` | — | 1 | No test functions; required matrix placeholder. |
| `tests/test_video.py` | `test_video9_import` | 50 | Valid public-export smoke test; weak behavioral signal. |
| `tests/test_video.py` | `TestVideoCoverage::test_get_clip_basic` | 76 |  |
| `tests/test_video.py` | `TestVideoCoverage::test_get_clip_raw` | 73 |  |
| `tests/test_video.py` | `TestVideoCoverage::test_get_length` | 73 |  |
| `tests/test_video.py` | `TestVideoCoverage::test_get_fps` | 73 |  |
| `tests/test_video.py` | `TestVideoCoverage::test_get_bitrate` | 73 |  |
| `tests/test_video.py` | `TestVideoCoverage::test_get_audio_bitrate` | 73 |  |
| `tests/test_video.py` | `TestVideoCoverage::test_get_resolution` | 73 |  |
| `tests/test_video.py` | `TestVideoCoverage::test_get_info` | 73 |  |
| `tests/test_video.py` | `TestVideoCoverage::test_video_instance_helpers` | 76 |  |
| `tests/test_video.py` | `test_video_class_getters_with_mocked_moviepy` | 76 |  |
| `tests/test_video.py` | `test_video_instance_wrappers_call_classmethods` | 76 |  |
| `tests/test_video_integration.py` | — | 1 | No test functions; required matrix placeholder. |
| `tests/test_video_integration_negative.py` | — | 1 | No test functions; required matrix placeholder. |
| `tests/test_video_negative.py` | `test_video_instance_requires_path` | 78 | Distinct canonical regression case. |
| `tests/test_wget.py` | `test_wget_import` | 50 | Valid public-export smoke test; weak behavioral signal. |
| `tests/test_wget.py` | `test_wget_callable_sets_url` | 66 | Mock-heavy interaction check; limited real implementation coverage. |
| `tests/test_wget.py` | `test_wget_download_creates_dir_and_handles_missing` | 84 |  |
| `tests/test_wget.py` | `test_wget_download_fallback_wget_path` | 78 |  |
| `tests/test_wget.py` | `test_wget_instance_call_merges_defaults` | 76 |  |
| `tests/test_wget.py` | `test_wget_download_recovers_with_alternate_path` | 81 |  |
| `tests/test_wget.py` | `test_wget_download_windows_extension` | 78 |  |
| `tests/test_wget.py` | `test_wget_download_no_check_certificate` | 78 |  |
| `tests/test_wget.py` | `test_wget_instance_sets_attrs_and_calls` | 76 |  |
| `tests/test_wget_integration.py` | — | 1 | No test functions; required matrix placeholder. |
| `tests/test_wget_integration_negative.py` | — | 1 | No test functions; required matrix placeholder. |
| `tests/test_wget_negative.py` | `test_wget_download_raises_on_missing_wget` | 75 | Distinct canonical regression case. |
| `tests/test_wget_negative.py` | `test_wget_callable_requires_url` | 78 | Distinct canonical regression case. |
| `tests/test_wget_negative.py` | `test_wget_fetch_requires_output` | 78 | Distinct canonical regression case. |
| `tests/test_wget_negative.py` | `test_wget_instance_requires_url_output` | 78 | Distinct canonical regression case. |
| `tests/test_wget_negative.py` | `test_wget_download_custom_path_error` | 80 | Distinct canonical regression case. |
| `tests/test_windows.py` | `test_windows9_import` | 50 | Valid public-export smoke test; weak behavioral signal. |
| `tests/test_windows.py` | `test_windows_getenv_sets_default` | 82 |  |
| `tests/test_windows.py` | `test_windows_getenv_handles_missing` | 76 |  |
| `tests/test_windows.py` | `test_windows_setenv` | 76 | Mock-heavy interaction check; limited real implementation coverage. |
| `tests/test_windows.py` | `test_windows_power_shell_policy` | 73 |  |
| `tests/test_windows.py` | `test_windows_dump_auditpol_handles_subprocess` | 61 | Mock-heavy interaction check; limited real implementation coverage. Wall-clock dependence adds timing-flake risk. |
| `tests/test_windows.py` | `test_windows_get_cmd_code_page_failure` | 78 |  |
| `tests/test_windows.py` | `test_windows_get_cmd_code_page_parsing` | 78 |  |
| `tests/test_windows.py` | `test_windows_fix_unicode_encode_error_safe` | 55 | Valid narrow contract. Only type/presence assertion; behavioral regression coverage is weak. |
| `tests/test_windows.py` | `test_windows_user_exists_calls_console` | 66 |  |
| `tests/test_windows.py` | `test_windows_get_cmd_code_page_debug_and_keyerror_fallback` | 79 |  |
| `tests/test_windows.py` | `test_windows_change_wallpaper` | 66 | Re-scored after removing shadowing/stale-suite interference. |
| `tests/test_windows.py` | `test_windows_getenv_system_scope` | 73 |  |
| `tests/test_windows.py` | `test_windows_remote_factory` | 73 |  |
| `tests/test_windows.py` | `test_windows_lock_calls_ctypes_non_windows10` | 73 | Mock-heavy interaction check; limited real implementation coverage. |
| `tests/test_windows.py` | `test_windows_import_winreg_sets_flag` | 66 |  |
| `tests/test_windows.py` | `test_windows_powershell_policy_set_success` | 73 |  |
| `tests/test_windows.py` | `test_windows_run_powershell_reuses_policy` | 73 |  |
| `tests/test_windows.py` | `test_windows_remote_system_ps_and_cmd` | 66 |  |
| `tests/test_windows.py` | `test_windows_remote_system_fix_run_ps_wraps_run_cmd` | 76 |  |
| `tests/test_windows.py` | `test_windows_instance_connect_and_methods` | 82 |  |
| `tests/test_windows.py` | `test_remote_system_winrm_fix_and_error` | 69 |  |
| `tests/test_windows.py` | `test_windows_remote_system_cmd_args` | 73 |  |
| `tests/test_windows.py` | `test_windows_remote_connect_sets_remote` | 82 |  |
| `tests/test_windows.py` | `test_windows_remote_shortcut_factory` | 55 | Valid narrow contract. Only type/presence assertion; behavioral regression coverage is weak. |
| `tests/test_windows.py` | `test_windows_set_cmd_code_page` | 78 |  |
| `tests/test_windows.py` | `test_windows_set_cmd_code_page_error` | 81 |  |
| `tests/test_windows.py` | `test_windows_fix_unicode_lockfile_safe` | 76 |  |
| `tests/test_windows.py` | `test_windows_fix_unicode_success_path` | 76 |  |
| `tests/test_windows.py` | `test_windows_fix_unicode_exception_safe_returns_previous_codepage` | 76 |  |
| `tests/test_windows.py` | `test_windows_user_exists_success` | 66 |  |
| `tests/test_windows.py` | `test_windows_user_exists_called_process` | 66 |  |
| `tests/test_windows.py` | `test_windows_user_create_success` | 55 | Valid narrow contract. Exercises private implementation detail; refactor-sensitive. |
| `tests/test_windows.py` | `test_windows_run_powershell_success` | 76 |  |
| `tests/test_windows.py` | `test_console_auto_decoding_unix_family_branch` | 66 |  |
| `tests/test_windows.py` | `test_os_name_linux_branch` | 73 |  |
| `tests/test_windows.py` | `test_file_get_mime_non_windows_import_magic` | 78 |  |
| `tests/test_windows.py` | `test_dir_copy_symlink_branch` | 71 |  |
| `tests/test_windows.py` | `test_archive_tar_filter_set_on_py312` | 70 | Exercises private implementation detail; refactor-sensitive. |
| `tests/test_windows.py` | `TestWindowsMissingCoverage::test_windows_init_with_remote_params` | 55 | Valid narrow contract. Only type/presence assertion; behavioral regression coverage is weak. |
| `tests/test_windows.py` | `TestWindowsMissingCoverage::test_windows_create_user_wrapper` | 76 | Mock-heavy interaction check; limited real implementation coverage. |
| `tests/test_windows.py` | `TestWindowsMissingCoverage::test_windows_remove_user_wrapper` | 73 | Mock-heavy interaction check; limited real implementation coverage. |
| `tests/test_windows.py` | `TestWindowsMissingCoverage::test_get_cmd_code_page_debug` | 73 | Skipped in current environment; platform/dependency branch not runtime-verified here. |
| `tests/test_windows.py` | `TestWindowsMissingCoverage::test_fix_unicode_encode_error_returns_previous_codepage` | 76 |  |
| `tests/test_windows_integration.py` | `test_file_hide_verbose_prints` | 71 | Distinct canonical regression case. |
| `tests/test_windows_integration.py` | `TestWindowsMissingCoverage::test_dump_auditpol_with_fast_name` | 78 |  |
| `tests/test_windows_integration.py` | `TestWindowsMissingCoverage::test_dump_auditpol_verbose` | 71 |  |
| `tests/test_windows_integration_negative.py` | — | 1 | No test functions; required matrix placeholder. |
| `tests/test_windows_negative.py` | `test_windows_getenv_missing_key` | 76 | Distinct canonical regression case. |
| `tests/test_windows_negative.py` | `test_windows_setenv_assert` | 72 | Distinct canonical regression case. |
| `tests/test_windows_negative.py` | `TestWindowsMissingCoverage::test_user_already_exists_error` | 70 | Exercises private implementation detail; refactor-sensitive. |
| `tests/test_windows_negative.py` | `TestWindowsMissingCoverage::test_user_doesnt_exist_error` | 70 | Exercises private implementation detail; refactor-sensitive. |
| `tests/test_windows_negative.py` | `TestWindowsMissingCoverage::test_user_not_implemented_error` | 70 | Exercises private implementation detail; refactor-sensitive. |
| `tests/test_windows_negative.py` | `TestWindowsMissingCoverage::test_user_failed_to_create_error` | 70 | Exercises private implementation detail; refactor-sensitive. |
| `tests/test_windows_negative.py` | `TestWindowsMissingCoverage::test_user_failed_to_remove_error` | 70 | Exercises private implementation detail; refactor-sensitive. |
| `tests/test_windows_negative.py` | `TestWindowsMissingCoverage::test_get_powershell_policy_error` | 75 | Distinct canonical regression case. |
| `tests/test_windows_negative.py` | `TestWindowsMissingCoverage::test_set_powershell_policy_error` | 75 | Distinct canonical regression case. |
| `tests/test_windows_negative.py` | `TestWindowsMissingCoverage::test_windows_lock_missing_windll` | 75 |  |
| `tests/test_windows_negative.py` | `TestWindowsMissingCoverage::test_remote_system_requires_winrm` | 72 |  |
| `tests/test_windows_negative.py` | `TestWindowsMissingCoverage::test_import_winreg_missing_module` | 75 |  |
| `tests/test_windows_negative.py` | `TestWindowsMissingCoverage::test_change_wallpaper_missing_windll` | 75 |  |
| `tests/test_windows_negative.py` | `test_windows_lock_version_guard` | 72 | Distinct canonical regression case. |
| `tests/test_windows_negative.py` | `test_windows_dump_auditpol_missing_permissions` | 72 | Re-scored after removing shadowing/stale-suite interference. |
| `tests/test_windows_negative.py` | `test_windows_instance_requires_remote_for_ps` | 78 | Distinct canonical regression case. |
| `tests/test_windows_negative.py` | `test_windows_instance_requires_remote_for_cmd` | 78 | Distinct canonical regression case. |
| `tests/test_windows_negative.py` | `test_windows_lock_fails_windows10` | 72 | Distinct canonical regression case. |
| `tests/test_windows_negative.py` | `test_windows_powershell_policy_set_error` | 75 |  |
| `tests/test_windows_negative.py` | `test_windows_fix_unicode_restore_on_error` | 70 | Exercises private implementation detail; refactor-sensitive. |
| `tests/test_windows_negative.py` | `test_windows_fix_unicode_lockfile_unsafe_raises` | 75 |  |
| `tests/test_windows_negative.py` | `test_windows_fix_unicode_restore_on_exception` | 85 |  |
| `tests/test_windows_negative.py` | `test_windows_user_invalid_username_type` | 70 | Exercises private implementation detail; refactor-sensitive. |
| `tests/test_windows_negative.py` | `test_windows_user_create_missing_password` | 70 | Exercises private implementation detail; refactor-sensitive. |
| `tests/test_windows_negative.py` | `test_windows_user_remove_missing` | 70 | Exercises private implementation detail; refactor-sensitive. |
| `tests/test_windows_negative.py` | `test_windows_user_create_output_error` | 70 | Exercises private implementation detail; refactor-sensitive. |
| `tests/test_windows_negative.py` | `test_windows_user_retry_on_called_process` | 67 | Exercises private implementation detail; refactor-sensitive. |
| `tests/test_windows_negative.py` | `test_windows_user_remove_called_process_gives_final_error` | 70 | Exercises private implementation detail; refactor-sensitive. |
| `tests/test_windows_negative.py` | `test_windows_run_powershell_error` | 75 |  |
