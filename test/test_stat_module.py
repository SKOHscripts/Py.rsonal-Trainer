import pytest
import yaml
import pandas as pd
import tempfile
import os
from src.stat_module import (
    load_training_data,
    extract_activity_stats,
    collect_all_stats,
    per_sport_stats,
    display_stats_tables
)


class TestLoadTrainingData:
    """Test suite for load_training_data function."""

    def test_load_valid_yaml_file(self):
        """Test loading a valid YAML file with training data."""
        # Create a temporary YAML file
        yaml_content = {
            'data': [
                {
                    'week_first_day': '2024-12-30',
                    'trail_running': [
                        {
                            'session_description': 'Trail',
                            'distance_km': 16.5,
                            'elevation_m': 319,
                            'time_min': 92,
                            'load': 189
                        }
                    ]
                }
            ]
        }

        with tempfile.NamedTemporaryFile(mode='w', suffix='.yml', delete=False) as f:
            yaml.dump(yaml_content, f)
            temp_path = f.name

        try:
            result = load_training_data(temp_path)
            assert isinstance(result, list)
            assert len(result) == 1
            assert result[0]['week_first_day'] == '2024-12-30'
            assert 'trail_running' in result[0]
        finally:
            os.unlink(temp_path)

    def test_load_nonexistent_file(self):
        """Test loading a non-existent file raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            load_training_data('nonexistent_file.yml')

    def test_load_invalid_yaml_structure(self):
        """Test loading YAML without 'data' key raises KeyError."""
        yaml_content = {'invalid_key': []}

        with tempfile.NamedTemporaryFile(mode='w', suffix='.yml', delete=False) as f:
            yaml.dump(yaml_content, f)
            temp_path = f.name

        try:
            with pytest.raises(KeyError):
                load_training_data(temp_path)
        finally:
            os.unlink(temp_path)

    def test_load_empty_data_list(self):
        """Test loading YAML with empty data list."""
        yaml_content = {'data': []}

        with tempfile.NamedTemporaryFile(mode='w', suffix='.yml', delete=False) as f:
            yaml.dump(yaml_content, f)
            temp_path = f.name

        try:
            result = load_training_data(temp_path)
            assert isinstance(result, list)
            assert len(result) == 0
        finally:
            os.unlink(temp_path)


class TestExtractActivityStats:
    """Test suite for extract_activity_stats function."""

    def test_extract_single_session_stats(self):
        """Test extracting stats for activity with single session."""
        week_data = {
            'week_first_day': '2024-12-30',
            'trail_running': [
                {
                    'session_description': 'Trail',
                    'distance_km': 16.5,
                    'elevation_m': 319,
                    'time_min': 92,
                    'load': 189
                }
            ]
        }

        result = extract_activity_stats(week_data, 'trail_running')

        assert result['time_min'] == 92
        assert result['distance_km'] == 16.5
        assert result['elevation_m'] == 319
        assert result['load'] == 189

    def test_extract_multiple_sessions_stats(self):
        """Test extracting stats for activity with multiple sessions."""
        week_data = {
            'interval_training': [
                {
                    'distance_km': 12.6,
                    'elevation_m': 10,
                    'time_min': 69,
                    'load': 158
                },
                {
                    'distance_km': 14.0,
                    'elevation_m': 341,
                    'time_min': 85,
                    'load': 156
                }
            ]
        }

        result = extract_activity_stats(week_data, 'interval_training')

        assert result['time_min'] == 154  # 69 + 85
        assert result['distance_km'] == 26.6  # 12.6 + 14.0
        assert result['elevation_m'] == 351  # 10 + 341
        assert result['load'] == 314  # 158 + 156

    def test_extract_nonexistent_activity(self):
        """Test extracting stats for non-existent activity returns zeros."""
        week_data = {'week_first_day': '2024-12-30'}

        result = extract_activity_stats(week_data, 'swimming')

        assert result['time_min'] == 0
        assert result['distance_km'] == 0
        assert result['elevation_m'] == 0
        assert result['load'] == 0

    def test_extract_missing_fields(self):
        """Test extracting stats when some fields are missing."""
        week_data = {
            'others': [
                {
                    'session_description': 'Weight training',
                    'time_min': 61
                    # missing distance_km, elevation_m, load
                }
            ]
        }

        result = extract_activity_stats(week_data, 'others')

        assert result['time_min'] == 61
        assert result['distance_km'] == 0
        assert result['elevation_m'] == 0
        assert result['load'] == 0

    def test_extract_empty_session_list(self):
        """Test extracting stats for activity with empty session list."""
        week_data = {'footing': []}

        result = extract_activity_stats(week_data, 'footing')

        assert result['time_min'] == 0
        assert result['distance_km'] == 0
        assert result['elevation_m'] == 0
        assert result['load'] == 0


class TestCollectAllStats:
    """Test suite for collect_all_stats function."""

    def test_collect_single_week_stats(self):
        """Test collecting stats for a single week."""
        weeks = [
            {
                'week_first_day': '2024-12-30',
                'trail_running': [
                    {
                        'distance_km': 16.5,
                        'elevation_m': 319,
                        'time_min': 92,
                        'load': 189
                    }
                ],
                'others': [
                    {
                        'time_min': 61
                    }
                ]
            }
        ]

        result = collect_all_stats(weeks)

        assert isinstance(result, pd.DataFrame)
        assert len(result) == 1
        assert result.iloc[0]['week_first_day'] == '2024-12-30'
        assert result.iloc[0]['trail_running_time_min'] == 92
        assert result.iloc[0]['trail_running_distance_km'] == 16.5
        assert result.iloc[0]['others_time_min'] == 61
        assert result.iloc[0]['week_total_time_min'] == 153  # 92 + 61

    def test_collect_multiple_weeks_stats(self):
        """Test collecting stats for multiple weeks."""
        weeks = [
            {
                'week_first_day': '2024-12-30',
                'trail_running': [{'time_min': 92, 'load': 189}]
            },
            {
                'week_first_day': '2025-01-06',
                'footing': [{'time_min': 54, 'distance_km': 10.4}]
            }
        ]

        result = collect_all_stats(weeks)

        assert len(result) == 2
        assert result.iloc[0]['trail_running_time_min'] == 92
        assert result.iloc[0]['footing_time_min'] == 0  # No footing in first week
        assert result.iloc[1]['footing_time_min'] == 54
        assert result.iloc[1]['trail_running_time_min'] == 0  # No trail running in second week

    def test_collect_empty_weeks_list(self):
        """Test collecting stats from empty weeks list."""
        weeks = []

        result = collect_all_stats(weeks)

        assert isinstance(result, pd.DataFrame)
        assert len(result) == 0

    def test_collect_week_with_comment(self):
        """Test collecting stats for week with comment."""
        weeks = [
            {
                'week_first_day': '2025-01-20',
                'week_comment': 'Raid',
                'trail_running': [{'time_min': 876, 'load': 1051}]
            }
        ]

        result = collect_all_stats(weeks)

        assert result.iloc[0]['week_comment'] == 'Raid'

    def test_collect_week_without_activities(self):
        """Test collecting stats for week with only date."""
        weeks = [
            {
                'week_first_day': '2025-02-17'
            }
        ]

        result = collect_all_stats(weeks)

        assert len(result) == 1
        assert result.iloc[0]['week_total_time_min'] == 0
        assert result.iloc[0]['week_total_distance_km'] == 0


class TestPerSportStats:
    """Test suite for per_sport_stats function."""

    def setup_method(self):
        """Set up test dataframe for per sport stats tests."""
        self.test_df = pd.DataFrame([
            {
                'week_first_day': '2024-12-30',
                'trail_running_time_min': 92,
                'trail_running_distance_km': 16.5,
                'trail_running_elevation_m': 319,
                'trail_running_load': 189,
                'others_time_min': 61,
                'others_distance_km': 0,
                'others_elevation_m': 0,
                'others_load': 0,
                'week_total_time_min': 153,
                'week_total_distance_km': 16.5
            },
            {
                'week_first_day': '2025-01-06',
                'trail_running_time_min': 124,
                'trail_running_distance_km': 20.0,
                'trail_running_elevation_m': 416,
                'trail_running_load': 203,
                'others_time_min': 105,
                'others_distance_km': 0,
                'others_elevation_m': 0,
                'others_load': 0,
                'week_total_time_min': 229,
                'week_total_distance_km': 20.0
            }
        ])

    def test_per_sport_without_total(self):
        """Test per sport stats without total row."""
        result = per_sport_stats(self.test_df, with_total=False)

        assert isinstance(result, pd.DataFrame)
        assert len(result) == 2  # trail_running and others

        # Check trail_running stats
        trail_row = result[result['activity'] == 'trail_running'].iloc[0]
        assert trail_row['time_min'] == 216  # 92 + 124
        assert trail_row['distance_km'] == 36.5  # 16.5 + 20.0
        assert trail_row['elevation_m'] == 735  # 319 + 416
        assert trail_row['load'] == 392  # 189 + 203

        # Check others stats
        others_row = result[result['activity'] == 'others'].iloc[0]
        assert others_row['time_min'] == 166  # 61 + 105

    def test_per_sport_with_total(self):
        """Test per sport stats with total row."""
        result = per_sport_stats(self.test_df, with_total=True)

        assert len(result) == 3  # trail_running, others, and TOTAL

        # Check TOTAL row
        total_row = result[result['activity'] == 'TOTAL'].iloc[0]
        assert total_row['time_min'] == 382  # 216 + 166
        assert total_row['distance_km'] == 36.5
        assert total_row['elevation_m'] == 735
        assert total_row['load'] == 392

    def test_per_sport_excludes_week_totals(self):
        """Test that week_total columns are excluded from sport stats."""
        result = per_sport_stats(self.test_df, with_total=False)

        # Should not include 'week_total' as an activity
        activities = result['activity'].tolist()
        assert 'week_total' not in activities
        assert len(activities) == 2  # Only trail_running and others

    def test_per_sport_empty_dataframe(self):
        """Test per sport stats with empty dataframe."""
        empty_df = pd.DataFrame()

        result = per_sport_stats(empty_df, with_total=False)

        assert isinstance(result, pd.DataFrame)
        assert len(result) == 0

    def test_per_sport_missing_columns(self):
        """Test per sport stats when some stat columns are missing."""
        incomplete_df = pd.DataFrame([
            {
                'week_first_day': '2024-12-30',
                'swimming_time_min': 55,
                'swimming_load': 58
                # Missing distance_km and elevation_m columns
            }
        ])

        result = per_sport_stats(incomplete_df, with_total=False)

        assert len(result) == 1
        swimming_row = result.iloc[0]
        assert swimming_row['activity'] == 'swimming'
        assert swimming_row['time_min'] == 55
        assert swimming_row['distance_km'] == 0  # Missing column defaults to 0
        assert swimming_row['elevation_m'] == 0  # Missing column defaults to 0
        assert swimming_row['load'] == 58


class TestDisplayStatsTables:
    """Test suite for display_stats_tables function."""

    def test_display_with_valid_file(self, capsys):
        """Test display function with valid YAML file."""
        yaml_content = {
            'data': [
                {
                    'week_first_day': '2024-12-30',
                    'trail_running': [
                        {
                            'distance_km': 16.5,
                            'elevation_m': 319,
                            'time_min': 92,
                            'load': 189
                        }
                    ]
                }
            ]
        }

        with tempfile.NamedTemporaryFile(mode='w', suffix='.yml', delete=False) as f:
            yaml.dump(yaml_content, f)
            temp_path = f.name

        try:
            display_stats_tables(temp_path)
            captured = capsys.readouterr()

            assert "==== STATISTIQUES HEBDOMADAIRES ====" in captured.out
            assert "==== STATISTIQUES GLOBALES PAR TYPE DE SPORT ====" in captured.out
            assert "2024-12-30" in captured.out
            assert "trail_running" in captured.out
        finally:
            os.unlink(temp_path)

    def test_display_with_nonexistent_file(self):
        """Test display function with non-existent file raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            display_stats_tables('nonexistent_file.yml')


class TestIntegration:
    """Integration tests for the complete workflow."""

    def test_complete_workflow(self):
        """Test complete workflow from YAML loading to stats computation."""
        yaml_content = {
            'data': [
                {
                    'week_first_day': '2024-12-30',
                    'trail_running': [
                        {
                            'distance_km': 16.5,
                            'elevation_m': 319,
                            'time_min': 92,
                            'load': 189
                        }
                    ],
                    'others': [
                        {
                            'session_description': 'Weight training',
                            'time_min': 61
                        }
                    ]
                },
                {
                    'week_first_day': '2025-01-06',
                    'footing': [
                        {
                            'distance_km': 10.4,
                            'elevation_m': 7,
                            'time_min': 54,
                            'load': 127
                        }
                    ]
                }
            ]
        }

        with tempfile.NamedTemporaryFile(mode='w', suffix='.yml', delete=False) as f:
            yaml.dump(yaml_content, f)
            temp_path = f.name

        try:
            # Test complete workflow
            weeks = load_training_data(temp_path)
            assert len(weeks) == 2

            df = collect_all_stats(weeks)
            assert len(df) == 2
            assert df.iloc[0]['trail_running_time_min'] == 92
            assert df.iloc[1]['footing_time_min'] == 54

            sport_stats = per_sport_stats(df, with_total=True)
            assert len(sport_stats) == 4  # trail_running, others, footing, TOTAL

            # Verify totals
            total_row = sport_stats[sport_stats['activity'] == 'TOTAL'].iloc[0]
            assert total_row['time_min'] == 207  # 92 + 61 + 54

        finally:
            os.unlink(temp_path)

    def test_workflow_with_complex_activities(self):
        """Test workflow with multi-word activity names."""
        yaml_content = {
            'data': [
                {
                    'week_first_day': '2025-02-03',
                    'interval_training': [
                        {
                            'distance_km': 12.6,
                            'time_min': 69,
                            'load': 158
                        },
                        {
                            'distance_km': 14.0,
                            'time_min': 85,
                            'load': 156
                        }
                    ]
                }
            ]
        }

        with tempfile.NamedTemporaryFile(mode='w', suffix='.yml', delete=False) as f:
            yaml.dump(yaml_content, f)
            temp_path = f.name

        try:
            weeks = load_training_data(temp_path)
            df = collect_all_stats(weeks)
            sport_stats = per_sport_stats(df, with_total=False)

            # Verify interval_training is preserved as complete name
            assert len(sport_stats) == 1
            assert sport_stats.iloc[0]['activity'] == 'interval_training'
            assert sport_stats.iloc[0]['time_min'] == 154  # 69 + 85
            assert sport_stats.iloc[0]['distance_km'] == 26.6  # 12.6 + 14.0

        finally:
            os.unlink(temp_path)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
