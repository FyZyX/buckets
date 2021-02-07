from sqlalchemy import create_engine
from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///nba.db', echo=True)
Base = declarative_base(bind=engine)


class Team(Base):
    __tablename__ = 'teams'

    id = Column(Integer, primary_key=True)
    city = Column(String)
    full_name = Column(String)
    nickname = Column(String)
    logo = Column(String)
    short_name = Column(String)
    all_star = Column(Integer)
    nba_franchise = Column(Integer)

    players = relationship('Player', back_populates='team')
    statistics = relationship('TeamStats', back_populates='team')

    # TODO: Create a relationship with leagues

    def __init__(self, team_id, city, full_name, nickname, logo, short_name,
                 all_star, nba_franchise):
        self.id = team_id
        self.city = city
        self.full_name = full_name
        self.nickname = nickname
        self.logo = logo
        self.short_name = short_name
        self.all_star = all_star
        self.nba_franchise = nba_franchise

    @classmethod
    def from_json(cls, team):
        return cls(
            team_id=int(team['teamId']),
            city=team['city'],
            full_name=team['fullName'],
            nickname=team['nickname'],
            logo=team['logo'],
            short_name=team['shortName'],
            all_star=int(team['allStar']),
            nba_franchise=int(team['nbaFranchise']),
        )

    def __repr__(self):
        return f"<{self.__class__}(full_name='{self.full_name}')>"


class Player(Base):
    __tablename__ = 'players'

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    team_id = Column(String, ForeignKey('teams.id'))
    years_pro = Column(Integer)
    college_name = Column(String)
    country = Column(String)
    date_of_birth = Column(String)
    affiliation = Column(String)
    start_nba = Column(String)
    height_in_meters = Column(Float)
    weight_in_kilograms = Column(Float)

    team = relationship('Team', back_populates='players')
    statistics = relationship('PlayerStats', back_populates='player')

    def __init__(self, player_id, first_name, last_name, team_id, years_pro,
                 college_name, country, date_of_birth, affiliation,
                 start_nba, height_in_meters, weight_in_kilograms):
        self.id = player_id
        self.first_name = first_name
        self.last_name = last_name
        self.team_id = team_id
        self.years_pro = years_pro
        self.college_name = college_name
        self.country = country
        self.date_of_birth = date_of_birth
        self.affiliation = affiliation
        self.start_nba = start_nba
        self.height_in_meters = height_in_meters
        self.weight_in_kilograms = weight_in_kilograms

    @classmethod
    def from_json(cls, player):
        return cls(
            player_id=int(player['playerId']),
            first_name=player['firstName'],
            last_name=player['lastName'],
            team_id=player['teamId'],
            years_pro=int(player['yearsPro']),
            college_name=player['collegeName'],
            country=player['country'],
            date_of_birth=player['dateOfBirth'],
            affiliation=player['affiliation'],
            start_nba=player['startNba'],
            height_in_meters=float(player['heightInMeters']),
            weight_in_kilograms=float(player['weightInKilograms']),
        )

    def __repr__(self):
        return f"<{self.__class__}({self.first_name} {self.last_name})>"


class Game(Base):
    __tablename__ = 'games'

    id = Column(Integer, primary_key=True)
    season_year = Column(String)
    league = Column(String)
    start_time_utc = Column(String)
    end_time_utc = Column(String)
    arena = Column(String)
    city = Column(String)
    country = Column(String)
    clock = Column(String)
    game_duration = Column(String)
    current_period = Column(String)
    halftime = Column(Boolean)
    end_of_period = Column(Boolean)
    season_stage = Column(Integer)
    status_short_game = Column(Integer)
    status_game = Column(String)
    home_id = Column(Integer, ForeignKey('teams.id'))
    home_score = Column(Integer)
    away_id = Column(Integer, ForeignKey('teams.id'))
    away_score = Column(Integer)

    # TODO: figure out backrefs for home and away team
    home_team = relationship('Team', foreign_keys=[home_id])
    away_team = relationship('Team', foreign_keys=[away_id])
    team_statistics = relationship('TeamStats', back_populates='game')
    player_statistics = relationship('PlayerStats', back_populates='game')

    def __init__(self, game_id, season_year, league, start_time_utc,
                 end_time_utc, arena, city, country, clock, game_duration,
                 current_period, halftime, end_of_period, season_stage,
                 status_short_game, status_game, home_id, home_score,
                 away_id, away_score):
        self.id = game_id
        self.season_year = season_year
        self.league = league
        self.start_time_utc = start_time_utc
        self.end_time_utc = end_time_utc
        self.arena = arena
        self.city = city
        self.country = country
        self.clock = clock
        self.game_duration = game_duration
        self.current_period = current_period
        self.halftime = halftime
        self.end_of_period = end_of_period
        self.season_stage = season_stage
        self.status_short_game = status_short_game
        self.status_game = status_game
        self.home_id = home_id
        self.home_score = home_score
        self.away_id = away_id
        self.away_score = away_score

    @classmethod
    def from_json(cls, game):
        from pprint import pprint
        pprint(game)
        game_id = int(game['gameId'])
        halftime = game['halftime']
        halftime = bool(int(halftime)) if halftime else None
        end_of_period = game['EndOfPeriod']
        end_of_period = bool(int(end_of_period)) if end_of_period else None
        season_stage = int(game['seasonStage'])
        status_short_game = int(game['statusShortGame'])
        home_id = int(game['hTeam']['teamId'])
        home_score = game['hTeam']['score']['points']
        home_score = int(home_score) if home_score else None
        away_id = int(game['vTeam']['teamId'])
        away_score = game['vTeam']['score']['points']
        away_score = int(away_score) if away_score else None

        return cls(
            game_id=game_id,
            season_year=game['seasonYear'],
            league=game['league'],
            start_time_utc=game['startTimeUTC'],
            end_time_utc=game['endTimeUTC'],
            arena=game['arena'],
            city=game['city'],
            country=game['country'],
            clock=game['clock'],
            game_duration=game['gameDuration'],
            current_period=game['currentPeriod'],
            halftime=halftime,
            end_of_period=end_of_period,
            season_stage=season_stage,
            status_short_game=status_short_game,
            status_game=game['statusGame'],
            home_id=home_id,
            home_score=home_score,
            away_id=away_id,
            away_score=away_score,
        )

    def __repr__(self):
        return f"<{self.__class__}({self.city} {self.start_time_utc})>"


class TeamStats(Base):
    __tablename__ = 'team_stats'

    game_id = Column(Integer, ForeignKey('games.id'), primary_key=True)
    team_id = Column(Integer, ForeignKey('teams.id'), primary_key=True)
    fast_break_points = Column(Integer)
    points_in_paint = Column(Integer)
    biggest_lead = Column(Integer)
    second_chance_points = Column(Integer)
    points_off_turnovers = Column(Integer)
    longest_run = Column(Integer)
    points = Column(Integer)
    fgm = Column(Integer)
    fga = Column(Integer)
    fgp = Column(Float)
    ftm = Column(Integer)
    fta = Column(Integer)
    ftp = Column(Float)
    tpm = Column(Integer)
    tpa = Column(Integer)
    tpp = Column(Float)
    off_reb = Column(Integer)
    def_reb = Column(Integer)
    tot_reb = Column(Integer)
    assists = Column(Integer)
    p_fouls = Column(Integer)
    steals = Column(Integer)
    turnovers = Column(Integer)
    blocks = Column(Integer)
    plus_minus = Column(Integer)
    minutes = Column(String)

    game = relationship('Game', back_populates='team_statistics')
    team = relationship('Team', back_populates='statistics')

    def __init__(self, game_id, team_id, fast_break_points, points_in_paint,
                 biggest_lead, second_chance_points, points_off_turnovers,
                 longest_run, points, fgm, fga, fgp, ftm, fta, ftp, tpm,
                 tpa, tpp, off_reb, def_reb, tot_reb, assists, p_fouls,
                 steals, turnovers, blocks, plus_minus, minutes):
        self.game_id = game_id
        self.team_id = team_id
        self.fast_break_points = fast_break_points
        self.points_in_paint = points_in_paint
        self.biggest_lead = biggest_lead
        self.second_chance_points = second_chance_points
        self.points_off_turnovers = points_off_turnovers
        self.longest_run = longest_run
        self.points = points
        self.fgm = fgm
        self.fga = fga
        self.fgp = fgp
        self.ftm = ftm
        self.fta = fta
        self.ftp = ftp
        self.tpm = tpm
        self.tpa = tpa
        self.tpp = tpp
        self.off_reb = off_reb
        self.def_reb = def_reb
        self.tot_reb = tot_reb
        self.assists = assists
        self.p_fouls = p_fouls
        self.steals = steals
        self.turnovers = turnovers
        self.blocks = blocks
        self.plus_minus = plus_minus
        self.minutes = minutes

    @classmethod
    def from_json(cls, team_stat):
        return cls(
            game_id=int(team_stat['gameId']),
            team_id=int(team_stat['teamId']),
            fast_break_points=int(team_stat['fastBreakPoints']),
            points_in_paint=int(team_stat['pointsInPaint']),
            biggest_lead=int(team_stat['biggestLead']),
            second_chance_points=int(team_stat['secondChancePoints']),
            points_off_turnovers=int(team_stat['pointsOffTurnovers']),
            longest_run=int(team_stat['longestRun']),
            points=int(team_stat['points']),
            fgm=int(team_stat['fgm']),
            fga=int(team_stat['fga']),
            fgp=float(team_stat['fgp']),
            ftm=int(team_stat['ftm']),
            fta=int(team_stat['fta']),
            ftp=float(team_stat['ftp']),
            tpm=int(team_stat['tpm']),
            tpa=int(team_stat['tpa']),
            tpp=float(team_stat['tpp']),
            off_reb=int(team_stat['offReb']),
            def_reb=int(team_stat['defReb']),
            tot_reb=int(team_stat['totReb']),
            assists=int(team_stat['assists']),
            p_fouls=int(team_stat['pFouls']),
            steals=int(team_stat['steals']),
            turnovers=int(team_stat['turnovers']),
            blocks=int(team_stat['blocks']),
            plus_minus=int(team_stat['plusMinus']),
            minutes=team_stat['min'],
        )

    def __repr__(self):
        return f"<{self.__class__}(game={self.game_id} team={self.team_id})>"


class PlayerStats(Base):
    __tablename__ = 'player_stats'

    game_id = Column(Integer, ForeignKey('games.id'), primary_key=True)
    team_id = Column(Integer, ForeignKey('teams.id'), primary_key=True)
    player_id = Column(Integer, ForeignKey('players.id'), primary_key=True)
    points = Column(Integer)
    position = Column(String)
    minutes = Column(String)
    fgm = Column(Integer)
    fga = Column(Integer)
    fgp = Column(Float)
    ftm = Column(Integer)
    fta = Column(Integer)
    ftp = Column(Float)
    tpm = Column(Integer)
    tpa = Column(Integer)
    tpp = Column(Float)
    off_reb = Column(Integer)
    def_reb = Column(Integer)
    tot_reb = Column(Integer)
    assists = Column(Integer)
    p_fouls = Column(Integer)
    steals = Column(Integer)
    turnovers = Column(Integer)
    blocks = Column(Integer)
    plus_minus = Column(Integer)

    game = relationship('Game', back_populates='player_statistics')
    player = relationship('Player', back_populates='statistics')

    def __init__(self, game_id, team_id, player_id, points, position,
                 minutes, fgm, fga, fgp, ftm, fta, ftp, tpm, tpa, tpp,
                 off_reb, def_reb, tot_reb, assists, p_fouls, steals,
                 turnovers, blocks, plus_minus):
        self.game_id = game_id
        self.team_id = team_id
        self.player_id = player_id
        self.points = points
        self.position = position
        self.minutes = minutes
        self.fgm = fgm
        self.fga = fga
        self.fgp = fgp
        self.ftm = ftm
        self.fta = fta
        self.ftp = ftp
        self.tpm = tpm
        self.tpa = tpa
        self.tpp = tpp
        self.off_reb = off_reb
        self.def_reb = def_reb
        self.tot_reb = tot_reb
        self.assists = assists
        self.p_fouls = p_fouls
        self.steals = steals
        self.turnovers = turnovers
        self.blocks = blocks
        self.plus_minus = plus_minus

    @classmethod
    def from_json(cls, team_stat):
        return cls(
            game_id=int(team_stat['gameId']),
            team_id=int(team_stat['teamId']),
            player_id=int(team_stat['playerId']),
            points=int(team_stat['points']),
            position=team_stat['pos'],
            minutes=team_stat['min'],
            fgm=int(team_stat['fgm']),
            fga=int(team_stat['fga']),
            fgp=float(team_stat['fgp']),
            ftm=int(team_stat['ftm']),
            fta=int(team_stat['fta']),
            ftp=float(team_stat['ftp']),
            tpm=int(team_stat['tpm']),
            tpa=int(team_stat['tpa']),
            tpp=float(team_stat['tpp']),
            off_reb=int(team_stat['offReb']),
            def_reb=int(team_stat['defReb']),
            tot_reb=int(team_stat['totReb']),
            assists=int(team_stat['assists']),
            p_fouls=int(team_stat['pFouls']),
            steals=int(team_stat['steals']),
            turnovers=int(team_stat['turnovers']),
            blocks=int(team_stat['blocks']),
            plus_minus=int(team_stat['plusMinus']),
        )

    def __repr__(self):
        return f"<{self.__class__}(game={self.game_id} team={self.team_id})>"


def create_all():
    Base.metadata.create_all()


if __name__ == '__main__':
    create_all()
