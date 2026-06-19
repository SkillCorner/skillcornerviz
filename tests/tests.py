import unittest
import numpy as np
import pandas as pd
from matplotlib.figure import Figure
from matplotlib.axes import Axes

from skillcornerviz.standard_plots import scatter_plot as sca
from skillcornerviz.standard_plots import swarm_violin_plot as svp
from skillcornerviz.standard_plots import bar_plot as bar
from skillcornerviz.standard_plots import radar_plot as rad
from skillcornerviz.standard_plots import summary_table as sumtable
from skillcornerviz.standard_plots import narrative_ranking_plot as rank
from skillcornerviz.standard_plots import zscore_dotplot as zscore
from skillcornerviz.standard_plots import table_grid as tgrid
from skillcornerviz.utils import skillcorner_game_intelligence_utils as gi
from skillcornerviz.utils import skillcorner_physical_utils as pu


######################
#    PLOT TESTING
######################

class BarPlot(unittest.TestCase):
    def setUp(self):
        self.df = pd.DataFrame({
            'player_name': [f'Player{i}' for i in range(15)],
            'distance': [float(i * 100) for i in range(15)],
        })

    def test_return_type(self):
        fig, ax = bar.plot_bar_chart(df=self.df, metric='distance', label='Distance')
        self.assertIsInstance(fig, Figure)
        self.assertIsInstance(ax, Axes)

    def test_title(self):
        fig, ax = bar.plot_bar_chart(self.df, 'distance', plot_title='Test Title')
        self.assertEqual(ax.get_title(), 'Test Title')


class RadarPlot(unittest.TestCase):
    def setUp(self):
        self.metrics = [
            'cross_receiver_runs', 'runs_in_behind', 'runs_ahead_of_the_ball',
            'overlap_runs', 'underlap_runs', 'support_runs', 'coming_short_runs',
            'dropping_off_runs', 'pulling_half_space_runs', 'pulling_wide_runs',
        ]
        data = {'player_name': ['Player A', 'Player B']}
        for m in self.metrics:
            data[m] = [1.0, 2.0]
            data[m + '_pct'] = [50.0, 75.0]
        self.df = pd.DataFrame(data)

    def test_return_type(self):
        fig, ax = rad.plot_radar(
            df=self.df,
            label='Player A',
            metrics=self.metrics,
            percentiles_precalculated=True,
        )
        self.assertIsInstance(fig, Figure)
        self.assertIsInstance(ax, Axes)


class ScatterPlot(unittest.TestCase):
    def setUp(self):
        rng = np.random.default_rng(42)
        n = 20
        self.df = pd.DataFrame({
            'player_name': [f'Player{i}' for i in range(n)],
            'metric_x': rng.uniform(5.0, 15.0, n).tolist(),
            'metric_y': rng.uniform(1.0, 8.0, n).tolist(),
        })

    def test_return_type(self):
        fig, ax = sca.plot_scatter(df=self.df, x_metric='metric_x', y_metric='metric_y')
        self.assertIsInstance(fig, Figure)
        self.assertIsInstance(ax, Axes)

    def test_title(self):
        fig, ax = sca.plot_scatter(
            df=self.df, x_metric='metric_x', y_metric='metric_y', plot_title='Test'
        )
        self.assertEqual(ax.get_title(), 'Test')


class SummaryTable(unittest.TestCase):
    def setUp(self):
        self.df = pd.DataFrame({
            'player_name': ['Player A', 'Player B', 'Player C', 'Player D'],
            'distance': [100.0, 200.0, 150.0, 180.0],
            'speed': [5.0, 6.0, 4.5, 5.5],
        })

    def test_return_type(self):
        fig, ax = sumtable.plot_summary_table(
            df=self.df,
            metrics=['distance', 'speed'],
            metric_col_names=['Distance', 'Speed'],
            highlight_group=['Player A', 'Player B'],
        )
        self.assertIsInstance(fig, Figure)
        self.assertIsInstance(ax, Axes)


class SwarmViolinPlot(unittest.TestCase):
    def setUp(self):
        rng = np.random.default_rng(42)
        n = 30
        self.df = pd.DataFrame({
            'player_name': [f'Player{i}' for i in range(n)],
            'distance': rng.uniform(5000.0, 12000.0, n).tolist(),
            'position': ['CB', 'CM', 'ST'] * 10,
        })

    def test_return_type(self):
        fig, ax = svp.plot_swarm_violin(
            df=self.df, x_metric='distance', y_metric='position',
            y_groups=['CB', 'CM', 'ST'],
        )
        self.assertIsInstance(fig, Figure)
        self.assertIsInstance(ax, Axes)


class NarrativeRankingPlot(unittest.TestCase):
    def setUp(self):
        rng = np.random.default_rng(42)
        n = 20
        self.df = pd.DataFrame({
            'player_name': [f'Player{i}' for i in range(n)],
            'distance_p90': rng.uniform(8.0, 14.0, n).tolist(),
            'sprint_count_p90': rng.uniform(1.0, 8.0, n).tolist(),
        })
        self.questions = {
            'Running': ['distance_p90', 'sprint_count_p90'],
        }

    def test_return_type(self):
        fig, ax = rank.plot_ranking(
            df=self.df,
            questions=self.questions,
            highlight_group=['Player0', 'Player1', 'Player2'],
        )
        self.assertIsInstance(fig, Figure)
        self.assertIsInstance(ax, Axes)


class ZscoreDotplot(unittest.TestCase):
    def setUp(self):
        rng = np.random.default_rng(42)
        n = 30
        self.df = pd.DataFrame({
            'player_name': [f'Player{i}' for i in range(n)],
            'distance_z': rng.standard_normal(n).tolist(),
            'sprint_z': rng.standard_normal(n).tolist(),
        })
        self.questions = {'Running': ['distance', 'sprint']}

    def test_return_type(self):
        fig, ax = zscore.plot_zscore_dotplot(
            df=self.df,
            questions=self.questions,
            primary_highlight_group=['Player0', 'Player1'],
            data_point_id='player_name',
            data_point_label='player_name',
        )
        self.assertIsInstance(fig, Figure)
        self.assertIsInstance(ax, Axes)


class TableGrid(unittest.TestCase):
    def setUp(self):
        rng = np.random.default_rng(42)
        n = 10
        self.df = pd.DataFrame({
            'team': [f'Team{i}' for i in range(n)],
            'points': rng.uniform(1.0, 3.0, n).tolist(),
            'distance_z': rng.standard_normal(n).tolist(),
            'sprint_z': rng.standard_normal(n).tolist(),
            'press_z': rng.standard_normal(n).tolist(),
        })

    def test_return_type(self):
        fig, ax = tgrid.plot_table_grid(
            df=self.df,
            metrics=['distance_z', 'sprint_z', 'press_z'],
            labels=['Distance', 'Sprint', 'Press'],
            data_point_id='team',
            highlight_group=['Team0', 'Team1', 'Team2'],
            sort_by='points',
        )
        self.assertIsInstance(fig, Figure)
        self.assertIsInstance(ax, Axes)


#####################
#  GI & PU Testing
#####################

class GetPer90(unittest.TestCase):
    def setUp(self):
        self.df = pd.DataFrame({
            'player_name': ['Player1', 'Player2', 'Player3'],
            'metric_per_match': [100, 200, 300],
            'minutes_played_per_match': [90, 180, 270]
        })

    def test_get_per_90(self):
        expected_output = pd.Series([100.0, 100.0, 100.0])
        result = gi.get_per_90(self.df, 'metric_per_match')
        pd.testing.assert_series_equal(result, expected_output)


class GetPer30TIP(unittest.TestCase):
    def setUp(self):
        self.df = pd.DataFrame({
            'player_name': ['Player1', 'Player2', 'Player3'],
            'metric_per_match': [100, 200, 300],
            'adjusted_min_tip_per_match': [10, 50, 90]
        })

    def test_get_per_30_tip(self):
        expected_output = pd.Series([300.0, 120.0, 100.0])
        result = gi.get_per_30_tip(self.df, 'metric_per_match')
        pd.testing.assert_series_equal(result, expected_output)


class AddPer30TIP(unittest.TestCase):
    def setUp(self):
        self.df = pd.DataFrame({
            'player_name': ['Player1', 'Player2', 'Player3'],
            'count_metric_per_match': [100, 200, 60],
            'adjusted_min_tip_per_match': [10, 60, 90]
        })

    def test_add_per_30_tip(self):
        expected_col = ['count_metric_per_30_tip']
        expected_df = pd.DataFrame({
            'player_name': ['Player1', 'Player2', 'Player3'],
            'count_metric_per_match': [100, 200, 60],
            'adjusted_min_tip_per_match': [10, 60, 90],
            'count_metric_per_30_tip': [300.0, 100.0, 20.0]
        })

        result_df, metrics = gi.add_per_30_tip_metrics(self.df)

        self.assertEqual(expected_col, metrics)
        pd.testing.assert_frame_equal(result_df, expected_df)


class AddPer90(unittest.TestCase):
    def setUp(self):
        self.df = pd.DataFrame({
            'player_name': ['Player1', 'Player2', 'Player3'],
            'count_metric_per_match': [100, 200, 60],
            'minutes_played_per_match': [45, 30, 90]
        })

    def test_add_per_90_metrics(self):
        expected_col = ['count_metric_per_90']
        expected_df = pd.DataFrame({
            'player_name': ['Player1', 'Player2', 'Player3'],
            'count_metric_per_match': [100, 200, 60],
            'minutes_played_per_match': [45, 30, 90],
            'count_metric_per_90': [200.0, 600.0, 60.0]
        })

        result_df, metrics = gi.add_per_90_metrics(self.df)

        self.assertEqual(expected_col, metrics)
        pd.testing.assert_frame_equal(result_df, expected_df)


class PhysicalUtils(unittest.TestCase):
    def setUp(self):
        self.df = pd.DataFrame({
            'player_name': ['Player1', 'Player2', 'Player3'],
            'metric_full_all': [100.0, 200.0, 60.0],
            'minutes_full_all': [45.0, 30.0, 90.0],
        })

    def test_add_p90(self):
        expected_df = pd.DataFrame({
            'player_name': ['Player1', 'Player2', 'Player3'],
            'metric_full_all': [100.0, 200.0, 60.0],
            'minutes_full_all': [45.0, 30.0, 90.0],
            'metric_per_90': [200.0, 600.0, 60.0],
        })
        df = pu.add_p90(self.df, 'metric')
        pd.testing.assert_frame_equal(expected_df, df)


class AddP30TIP(unittest.TestCase):
    def setUp(self):
        self.df = pd.DataFrame({
            'player_name': ['Player1', 'Player2', 'Player3'],
            'metric_full_tip': [100.0, 50.0, 60.0],
            'minutes_full_tip': [10.0, 25.0, 90.0],
        })

    def test_add_p30_tip(self):
        pu.add_p30_tip(self.df, 'metric')
        expected = pd.Series([300.0, 60.0, 20.0], name='metric_per_30_tip')
        pd.testing.assert_series_equal(self.df['metric_per_30_tip'], expected)


class AddP60BIP(unittest.TestCase):
    def setUp(self):
        self.df = pd.DataFrame({
            'player_name': ['Player1', 'Player2', 'Player3'],
            'metric_full_tip': [50.0, 30.0, 20.0],
            'metric_full_otip': [20.0, 50.0, 40.0],
            'minutes_full_tip': [20.0, 30.0, 60.0],
            'minutes_full_otip': [10.0, 20.0, 30.0],
        })

    def test_add_p60_bip(self):
        pu.add_p60_bip(self.df, 'metric')
        # Player1: (50+20)/(20+10)*60 = 140.0
        # Player2: (30+50)/(30+20)*60 = 96.0
        # Player3: (20+40)/(60+30)*60 = 40.0
        expected = pd.Series([140.0, 96.0, 40.0], name='metric_per_60_bip')
        pd.testing.assert_series_equal(self.df['metric_per_60_bip'], expected)


if __name__ == '__main__':
    unittest.main()
