import datetime
from datetime import datetime
from datetime import timedelta
from datetime import date
from datetime import time
import dateutil
from dateutil import easter

import cathcal


class RomanCalendar():
	year = None
	easter = None
	christmas = None
	feast_days = {}

	def __init__(self,year=datetime.now().year):
		if year in range(9999):
			self.year = year
		else:
			raise ValueError, 'year must be between 1 and 9999'
		self._set_easter(self.year)
		self._set_christmas(self.year)

	def _set_easter(self, year=None):
		if year is None:
			year = self.year
		self.easter = easter.easter(year) 
		d = self.easter.strftime("%m/%d")
		self.feast_days[d] = 'Solemnity of The Resurrection - Solemnity'
		
	def _set_christmas(self, year=None):
		if year is None:
			year = self.year
		self.christmas = self.easter.replace(year, month=12, day=25)
		self.feast_days['12/25'] = 'Solemnity of the Nativity of Our Lord - Solemnity'




class RomanCalendar1962(RomanCalendar):
	cal = None
	sundays_after_pentecost = None
	advent = None
	epiphany = None
	octave_of_epiphany = None
	septuagesima = None
	ash_wed = None
	pentecost = None
	trinity_sunday = None
	corpus_cristi = None
	liturgical_season = None
	feast_days = { 
		'1/1': 'Octave of Christmas, Solemnity of Mary, Mother of God - Solemnity',
		'1/2': 'Saints Basil the Great and Gregory Nazianzen, bishops and doctors - Memorial',
		'1/3': 'The Most Holy Name of Jesus - Optional Memorial',
		'1/4': 'Feria',
		'1/5': 'Feria',
		'1/6': 'Epiphany', 
		'1/7': 'Saint Raymond of Penafort, priest - Optional Memorial',
		'1/8': 'Feria',
		'1/9': 'Feria',
		'1/10': 'Feria',
		'1/11': 'Feria',
		'1/12': 'Feria',
		'1/13': 'Saint Hilary of Poitiers, bishop and doctor - Optional Memorial',
		'1/14': 'Feria',
		'1/15': 'Feria',
		'1/16': 'Feria',
		'1/17': 'Saint Anthony of Egypt, abbot - Memorial',
		'1/18': 'Feria',
		'1/19': 'Feria',
		'1/20': 'Saint Fabian, pope and martyr; or Saint Sebastian, martyr - Optional Memorial',
		'1/21': 'Saint Agnes, virgin and martyr - Memorial',
		'1/22': 'Saint Vincent, deacon and martyr - Optional Memorial',
		'1/23': 'Feria',
		'1/24': 'Saint Francis de Sales, bishop and doctor - Memorial',
		'1/25': 'The Conversion of Saint Paul, apostle - Feast',
		'1/26': 'Saints Timothy and Titus, bishops - Memorial',
		'1/27': 'Saint Angela Merici, virgin - Optional Memorial',
		'1/28': 'Saint Thomas Aquinas, priest and doctor - Memorial',
		'1/29': 'Feria',
		'1/30': 'Feria',
		'1/31': 'Saint John Bosco, priest - Memorial',
		'2/1': 'Feria',
		'2/2': 'Presentation of the Lord - Feast',
		'2/3': 'Saint Blase, bishop and martyr, or Saint Ansgar, bishop - Optional Memorial',
		'2/4': 'Feria',
		'2/5': 'Saint Agatha, virgin and martyr - Memorial',
		'2/6': 'Saints Paul Miki and companions, martyrs - Memorial',
		'2/7': 'Feria',
		'2/8': 'Saint Jerome Emiliani or Saint Josephine Bakhita, virgin - Optional Memorial',
		'2/9': 'Feria',
		'2/10': 'Saint Scholastica, virgin - Memorial',
		'2/11': 'Our Lady of Lourdes - Optional Memorial',
		'2/12': 'Feria',
		'2/13': 'Feria',
		'2/14': 'Saints Cyril, monk, and Methodius, bishop - Memorial',
		'2/15': 'Feria',
		'2/16': 'Feria',
		'2/17': 'Seven Holy Founders of the Servite Order - Optional Memorial',
		'2/18': 'Feria',
		'2/19': 'Feria',
		'2/20': 'Feria',
		'2/21': 'Saint Peter Damian, bishop and doctor of the Church - Optional Memorial',
		'2/22': 'Chair of Saint Peter, apostle - Feast',
		'2/23': 'Saint Polycarp, bishop and martyr - Memorial',
		'2/24': 'Feria',
		'2/25': 'Feria',
		'2/26': 'Feria',
		'2/27': 'Feria',
		'2/28': 'Feria',
		'2/29': 'Feria',
		'3/1': 'Feria',
		'3/2': 'Feria',
		'3/3': 'Feria',
		'3/4': 'Saint Casimir - Optional Memorial',
		'3/5': 'Feria',
		'3/6': 'Feria',
		'3/7': 'Saints Perpetua and Felicity, martyrs - Memorial',
		'3/8': 'Saint John of God, religious - Optional Memorial',
		'3/9': 'Saint Frances of Rome, religious - Optional Memorial',
		'3/10': 'Feria',
		'3/11': 'Feria',
		'3/12': 'Feria',
		'3/13': 'Feria',
		'3/14': 'Feria',
		'3/15': 'Feria',
		'3/16': 'Feria',
		'3/17': 'Saint Patrick, bishop - Optional Memorial',
		'3/18': 'Saint Cyril of Jerusalem, bishop and doctor - Optional Memorial',
		'3/19': 'Saint Joseph Husband of the Blessed Virgin Mary - Solemnity',
		'3/20': 'Feria',
		'3/21': 'Feria',
		'3/22': 'Feria',
		'3/23': 'Saint Turibius of Mogrovejo, bishop - Optional Memorial',
		'3/24': 'Feria',
		'3/25': 'Annunciation of the Lord - Solemnity',
		'3/26': 'Feria',
		'3/27': 'Feria',
		'3/28': 'Feria',
		'3/29': 'Feria',
		'3/30': 'Feria',
		'3/31': 'Feria',
		'4/1': 'Feria',
		'4/2': 'Saint Francis of Paola, hermit - Optional Memorial',
		'4/3': 'Feria',
		'4/4': 'Saint Isidore, bishop and doctor of the Church- Optional Memorial',
		'4/5': 'Saint Vincent Ferrer, priest - Optional Memorial',
		'4/6': 'Feria',
		'4/7': 'Saint John Baptist de la Salle, priest - Memorial',
		'4/8': 'Feria',
		'4/9': 'Feria',
		'4/10': 'Feria',
		'4/11': 'Saint Stanislaus, bishop and martyr - Memorial',
		'4/12': 'Feria',
		'4/13': 'Saint Martin I, pope and martyr - Optional Memorial',
		'4/14': 'Feria',
		'4/15': 'Feria',
		'4/16': 'Feria',
		'4/17': 'Feria',
		'4/18': 'Feria',
		'4/19': 'Feria',
		'4/20': 'Feria',
		'4/21': 'Saint Anselm of Canterbury, bishop and doctor of the Church - Optional Memorial',
		'4/22': 'Feria',
		'4/23': 'Saint George, martyr, or Saint Adalbert, bishop and martyr - Optional Memorial',
		'4/24': 'Saint Fidelis of Sigmaringen, priest and martyr - Optional Memorial',
		'4/25': 'Saint Mark the Evangelist - Feast',
		'4/26': 'Feria',
		'4/27': 'Feria',
		'4/28': 'Saint Peter Chanel, priest and martyr; or Saint Louis Marie de Montfort, priest - Optional Memorial',
		'4/29': 'Saint Catherine of Siena, virgin and doctor of the Church - Memorial',
		'4/30': 'Saint Pius V, pope - Optional Memorial',
		'5/1': 'Saint Joseph the Worker - Optional Memorial',
		'5/2': 'Saint Athanasius, bishop and doctor - Memorial',
		'5/3': 'Saints Philip and James, Apostles - Feast',
		'5/4': 'Feria',
		'5/5': 'Feria',
		'5/6': 'Feria',
		'5/7': 'Feria',
		'5/8': 'Feria',
		'5/9': 'Feria',
		'5/10': 'Feria',
		'5/11': 'Feria',
		'5/12': 'Saints Nereus and Achilleus, martyrs or Saint Pancras, martyr - Optional Memorial',
		'5/13': 'Our Lady of Fatima - Optional Memorial',
		'5/14': 'Saint Matthias the Apostle - Feast',
		'5/15': 'Feria',
		'5/16': 'Feria',
		'5/17': 'Feria',
		'5/18': 'Saint John I, pope and martyr - Optional Memorial',
		'5/19': 'Feria',
		'5/20': 'Saint Bernardine of Siena, priest - Optional Memorial',
		'5/21': 'Saint Christopher Magallanes and companions, martyrs - Optional Memorial',
		'5/22': 'Saint Rita of Cascia - Optional Memorial',
		'5/23': 'Feria',
		'5/24': 'Feria',
		'5/25': 'Saint Bede the Venerable, priest and doctor; or Saint Gregory VII, pope or Saint Mary Magdalene de Pazzi, virgin - Optional Memorial',
		'5/26': 'Saint Philip Neri, priest - Memorial',
		'5/27': 'Saint Augustine (Austin) of Canterbury, bishop - Optional Memorial',
		'5/28': 'Feria',
		'5/29': 'Feria',
		'5/30': 'Feria',
		'5/31': 'Visitation of the Blessed Virgin Mary - Feast',
		'6/1': 'Saint Justin Martyr - Memorial',
		'6/2': 'Saints Marcellinus and Peter, martyrs - Optional Memorial',
		'6/3': 'Saints Charles Lwanga and companions, martyrs - Memorial',
		'6/4': 'Feria',
		'6/5': 'Saint Boniface, bishop and martyr - Memorial',
		'6/6': 'Saint Norbert, bishop - Optional Memorial',
		'6/7': 'Feria',
		'6/8': 'Feria',
		'6/9': 'Saint Ephrem, deacon and doctor - Optional Memorial',
		'6/10': 'Feria',
		'6/11': 'Saint Barnabas the Apostle - Memorial',
		'6/12': 'Feria',
		'6/13': 'Saint Anthony of Padua, priest and doctor - Memorial',
		'6/14': 'Feria',
		'6/15': 'Feria',
		'6/16': 'Feria',
		'6/17': 'Feria',
		'6/18': 'Feria',
		'6/19': 'Saint Romuald, abbot - Optional Memorial',
		'6/20': 'Feria',
		'6/21': 'Saint Aloysius Gonzaga, religious - Memorial',
		'6/22': 'Saint Paulinus of Nola, bishop or Saints John Fisher and Thomas More, martyrs - Optional Memorial',
		'6/23': 'Feria',
		'6/24': 'Birth of Saint John the Baptist - Solemnity',
		'6/25': 'Feria',
		'6/26': 'Feria',
		'6/27': 'Saint Cyril of Alexandria, bishop and doctor - Optional Memorial',
		'6/28': 'Saint Irenaeus, bishop and martyr - Memorial',
		'6/29': 'Saints Peter and Paul, Apostles - Solemnity',
		'6/30': 'First Martyrs of the Church of Rome - Optional Memorial',
		'7/1': 'Feria',
		'7/2': 'Feria',
		'7/3': 'Saint Thomas the Apostle - Feast',
		'7/4': 'Saint Elizabeth of Portugal - Optional Memorial',
		'7/5': 'Saint Anthony Zaccaria, priest - Optional Memorial',
		'7/6': 'Saint Maria Goretti, virgin and martyr - Memorial',
		'7/7': 'Feria',
		'7/8': 'Feria',
		'7/9': 'Saint Augustine Zhao Rong and companions, martyrs - Optional Memorial',
		'7/10': 'Feria',
		'7/11': 'Saint Benedict, abbot - Memorial',
		'7/12': 'Feria',
		'7/13': 'Saint Henry - Optional Memorial',
		'7/14': 'Saint Camillus de Lellis, priest - Optional Memorial',
		'7/15': 'Saint Bonaventure, bishop and doctor - Memorial',
		'7/16': 'Our Lady of Mount Carmel - Optional Memorial',
		'7/17': 'Feria',
		'7/18': 'Feria',
		'7/19': 'Feria',
		'7/20': 'Saint Apollinaris - Optional Memorial',
		'7/21': 'Saint Lawrence of Brindisi, priest and doctor - Optional Memorial',
		'7/22': 'Saint Mary Magdalene - Memorial',
		'7/23': 'Saint Birgitta, religious- Optional Memorial',
		'7/24': 'Saint Sharbel Makhluf, hermit - Optional Memorial',
		'7/25': 'Saint James, apostle - Feast',
		'7/26': 'Saints Joachim and Anne - Memorial',
		'7/27': 'Feria',
		'7/28': 'Feria',
		'7/29': 'Saint Martha - Memorial',
		'7/30': 'Saint Peter Chrysologus, bishop and doctor - Optional Memorial',
		'7/31': 'Saint Ignatius of Loyola, priest - Memorial',
		'8/1': 'Saint Alphonsus Maria de Liguori, bishop and doctor of the Church - Memorial',
		'8/2': 'Saint Eusebius of Vercelli, bishop, or Saint Peter Julian Eymard, priest - Optional Memorial',
		'8/3': 'Feria',
		'8/4': 'Saint Jean Vianney (the Cure of Ars), priest - Memorial',
		'8/5': 'Dedication of the Basilica di Santa Maria Maggiore - Optional Memorial',
		'8/6': 'Transfiguration of the Lord - Feast',
		'8/7': 'Saint Sixtus II, pope, and companions, martyrs, or Saint Cajetan, priest - Optional Memorial',
		'8/8': 'Saint Dominic, priest - Memorial',
		'8/9': 'Saint Teresa Benedicta of the Cross (Edith Stein), virgin and martyr - Optional Memorial',
		'8/10': 'Saint Lawrence, deacon and martyr - Feast',
		'8/11': 'Saint Clare, virgin - Memorial',
		'8/12': 'Saint Jane Frances de Chantal, religious - Optional Memorial',
		'8/13': 'Saints Pontian, pope, and Hippolytus, priest, martyrs - Optional Memorial',
		'8/14': 'Saint Maximilian Mary Kolbe, priest and martyr - Memorial',
		'8/15': 'Assumption of the Blessed Virgin Mary - Solemnity',
		'8/16': 'Saint Stephen of Hungary - Optional Memorial',
		'8/17': 'Feria',
		'8/18': 'Feria',
		'8/19': 'Saint John Eudes, priest - Optional Memorial',
		'8/20': 'Saint Bernard of Clairvaux, abbot and doctor of the Church - Memorial',
		'8/21': 'Saint Pius X, pope - Memorial',
		'8/22': 'Queenship of Blessed Virgin Mary - Memorial',
		'8/23': 'Saint Rose of Lima, virgin - Optional Memorial',
		'8/24': 'Saint Bartholomew the Apostle - Feast',
		'8/25': 'Saint Louis or Saint Joseph of Calasanz, priest - Optional Memorial',
		'8/26': 'Feria',
		'8/27': 'Saint Monica - Memorial',
		'8/28': 'Saint Augustine of Hippo, bishop and doctor of the Church - Memorial',
		'8/29': 'The Beheading of Saint John the Baptist, martyr - Memorial',
		'8/30': 'Feria',
		'8/31': 'Feria',
		'9/1': 'Feria',
		'9/2': 'Feria',
		'9/3': 'Saint Gregory the Great, pope and doctor - Memorial',
		'9/4': 'Feria',
		'9/5': 'Feria',
		'9/6': 'Feria',
		'9/7': 'Feria',
		'9/8': 'Birth of the Blessed Virgin Mary - Feast',
		'9/9': 'Saint Peter Claver, priest - Optional Memorial',
		'9/10': 'Feria',
		'9/11': 'Feria',
		'9/12': 'Holy Name of the Blessed Virgin Mary - Optional Memorial',
		'9/13': 'Saint John Chrysostom, bishop and doctor - Memorial',
		'9/14': 'Triumph of the Holy Cross - Feast',
		'9/15': 'Our Lady of Sorrows - Memorial',
		'9/16': 'Saints Cornelius, pope, and Cyprian, bishop, martyrs - Memorial',
		'9/17': 'Saint Robert Bellarmine, bishop and doctor - Optional Memorial',
		'9/18': 'Feria',
		'9/19': 'Saint Januarius, bishop and martyr - Optional Memorial',
		'9/20': 'Saint Andrew Kim Taegon, priest, and Paul Chong Hasang and companions, martyrs - Memorial',
		'9/21': 'Saint Matthew the Evangelist, Apostle, Evangelist - Feast',
		'9/22': 'Feria',
		'9/23': 'Saint Pio of Pietrelcina (Padre Pio), priest - Memorial',
		'9/24': 'Feria',
		'9/25': 'Feria',
		'9/26': 'Saints Cosmas and Damian, martyrs - Optional Memorial',
		'9/27': 'Saint Vincent de Paul, priest - Memorial',
		'9/28': 'Saints Lorenzo Ruiz and companions, martyrs - Memorial',
		'9/29': 'Saints Michael, Gabriel and Raphael, Archangels - Feast',
		'9/30': 'Saint Jerome, priest and doctor - Memorial',
		'10/1': 'Saint Therese of the Child Jesus, virgin and doctor - Memorial',
		'10/2': 'Guardian Angels - Memorial',
		'10/3': 'Feria',
		'10/4': 'Saint Francis of Assisi - Memorial',
		'10/5': 'Feria',
		'10/6': 'Saint Bruno, priest - Optional Memorial',
		'10/7': 'Our Lady of the Rosary - Memorial',
		'10/8': 'Feria',
		'10/9': 'Saint Denis and companions, martyrs or Saint John Leonardi, priest - Optional Memorial',
		'10/10': 'Feria',
		'10/11': 'Feria',
		'10/12': 'Feria',
		'10/13': 'Feria',
		'10/14': 'Saint Callistus I, pope and martyr - Optional Memorial',
		'10/15': 'Saint Teresa of Jesus, virgin and doctor - Memorial',
		'10/16': 'Saint Hedwig, religious or Saint Margaret Mary Alacoque, virgin - Optional Memorial',
		'10/17': 'Saint Ignatius of Antioch, bishop and martyr - Memorial',
		'10/18': 'Saint Luke the Evangelist - Feast',
		'10/19': 'Saints Jean de Brebeuf, Isaac Jogues, priests and companions, Martyrs or Saint Paul of the Cross, priest - Optional Memorial',
		'10/20': 'Feria',
		'10/21': 'Feria',
		'10/22': 'Feria',
		'10/23': 'Saint John of Capistrano, priest - Optional Memorial',
		'10/24': 'Saint Anthony Mary Claret, bishop - Optional Memorial',
		'10/25': 'Feria',
		'10/26': 'Feria',
		'10/27': 'Feria',
		'10/28': 'Saint Simon and Saint Jude, apostles - Feast',
		'10/29': 'Feria',
		'10/30': 'Feria',
		'10/31': 'Feria',
		'11/1': 'All Saints - Solemnity',
		'11/2': 'All Souls - ranked with solemnities',
		'11/3': 'Saint Martin de Porres, religious - Optional Memorial',
		'11/4': 'Saint Charles Borromeo, bishop - Memorial',
		'11/5': 'Feria',
		'11/6': 'Feria',
		'11/7': 'Feria',
		'11/8': 'Feria',
		'11/9': 'Dedication of the Lateran basilica - Feast',
		'11/10': 'Saint Leo the Great, pope and doctor - Memorial',
		'11/11': 'Saint Martin of Tours, bishop - Memorial',
		'11/12': 'Saint Josaphat, bishop and martyr - Memorial',
		'11/13': 'Feria',
		'11/14': 'Feria',
		'11/15': 'Saint Albert the Great, bishop and doctor - Optional Memorial',
		'11/16': 'Saint Margaret of Scotland or Saint Gertrude the Great, virgin - Optional Memorial',
		'11/17': 'Saint Elizabeth of Hungary, religious - Memorial',
		'11/18': 'Dedication of the basilicas of Saints Peter and Paul, Apostles - Optional Memorial',
		'11/19': 'Feria',
		'11/20': 'Feria',
		'11/21': 'Presentation of the Blessed Virgin Mary - Memorial',
		'11/22': 'Saint Cecilia - Memorial',
		'11/23': 'Saint Clement I, pope and martyr or Saint Columban, religious - Optional Memorial',
		'11/24': 'Saint Andrew Dung Lac and his companions, martyrs - Memorial',
		'11/25': 'Saint Catherine of Alexandria - Optional Memorial',
		'11/26': 'Feria',
		'11/27': 'Feria',
		'11/28': 'Feria',
		'11/29': 'Feria',
		'11/30': 'Saint Andrew the Apostle - Feast',
		'12/1': 'Feria',
		'12/2': 'Feria',
		'12/3': 'Saint Francis Xavier, priest - Memorial',
		'12/4': 'Saint John Damascene, priest and doctor - Optional Memorial',
		'12/5': 'Feria',
		'12/6': 'Saint Nicholas, bishop - Optional Memorial',
		'12/7': 'Saint Ambrose, bishop and doctor - Memorial',
		'12/8': 'Immaculate Conception of the Blessed Virgin Mary - Solemnity',
		'12/9': 'Saint Juan Diego - Optional Memorial',
		'12/10': 'Feria',
		'12/11': 'Saint Damasus I, pope - Optional Memorial',
		'12/12': 'Our Lady of Guadalupe - Optional Memorial',
		'12/13': 'Saint Lucy of Syracuse, virgin and martyr - Memorial',
		'12/14': 'Saint John of the Cross, priest and doctor - Memorial',
		'12/15': 'Feria',
		'12/16': 'Feria',
		'12/17': 'Feria',
		'12/18': 'Feria',
		'12/19': 'Feria',
		'12/20': 'Feria',
		'12/21': 'Saint Peter Canisius, priest and doctor - Optional Memorial',
		'12/22': 'Feria',
		'12/23': 'Saint John of Kanty, priest - Optional Memorial',
		'12/24': 'Feria',
		'12/25': 'Nativity of the Lord - Solemnity',
		'12/26': 'Saint Stephen, the first martyr - Feast',
		'12/27': 'Saint John the Apostle and evangelist - Feast',
		'12/28': 'Holy Innocents, martyrs - Feast',
		'12/29': 'Saint Thomas Becket, bishop and martyr - Optional Memorial',
		'12/30': 'Feria (Sixth Day within the Octave of Christmas)',
		'12/31': 'Saint Sylvester I, pope - Optional Memorial' 
	}
	
	def __init__(self,year=datetime.now().year):
		"""__init__()
		RomanCalendar1962 class constructor
		"""
		RomanCalendar.__init__(self,year)
		self._set_first_sunday_in_advent()
		self._set_epiphany()
		self._set_octave_of_epiphany()
		self._set_septuagesima()
		self._set_ash_wednesday()
		self._set_pentecost_sunday()
		self._set_trinity_sunday()
		self._set_corpus_cristi()
		self._sundays_after_pentecost()

		# determine season based on current date
	
	def _sundays_after_pentecost(self):
		sundays_after_pentecost = 1
		d = self.pentecost + timedelta(weeks=1)
		while d < self.advent:
			d = d + timedelta(days=1)
			if d.weekday() == 6:
				sundays_after_pentecost = sundays_after_pentecost + 1
		self.sundays_after_pentecost = sundays_after_pentecost
	
	def _set_first_sunday_in_advent(self, year=None):
		if self.christmas is not None:
			self.advent = self.christmas - timedelta(days=22)
			while self.advent.weekday() is not 6:
				self.advent = self.advent - timedelta(days=1)
			d = self.advent.strftime("%m/%d")
			if self.feast_days[d] is not 'Feria': 
				optional_feast = self.feast_days[d]
				self.feast_days[d] = "First Sunday of Advent (%s)"%(optional_feast)
			self.feast_days[d] = "First Sunday of Advent"

	def _set_christmas(self, year=None):
		# this is an ugly hack, I know, but I'm a porr, lazy, programmer... 
		self.christmas = self.easter.replace(year=self.year, month=12, day=25)
		self.feast_days['12/25'] = 'Solemnity of the Nativity of Our Lord'

	def _set_epiphany(self, year=None):
		self.epiphany = self.christmas.replace(year=self.year, month=1, day=6)
		self.feast_days['1/6'] = 'Feast of Epiphany'

	def _set_octave_of_epiphany(self, year=None):
		if self.epiphany is not None:
			self.octave_of_epiphany = self.epiphany + timedelta(days=8)

	def _set_septuagesima(self, year=None):
		if self.easter is not None:
			self.septuagesima = self.easter - timedelta(weeks=9)
			d = self.septuagesima.strftime("%m/%d")
			self.feast_days['%s' % d] = 'Septuagesima Sunday'
	
	def _set_ash_wednesday(self, year=None):
		if self.easter is not None:
			self.ash_wed = self.easter - timedelta(days=46)

	def _set_pentecost_sunday(self,year=None):
		if self.easter is not None:
			self.pentecost = self.easter + timedelta(weeks=7)
	
	def _set_trinity_sunday(self, year=None):
		if self.pentecost is not None:
			self.trinity_sunday = self.pentecost + timedelta(weeks=1)

	def _set_corpus_cristi(self, year=None):
		if self.trinity_sunday is not None:
			self.corpus_cristi = self.trinity_sunday + timedelta(days=4)

	def get_feast(self, d=date(datetime.now().year, datetime.now().month, datetime.now().day)):
		monthday = "%s/%s"%(d.month, d.day)
		if monthday in self.feast_days:
			return self.feast_days[monthday]
	
	def get_season(self, date=date(datetime.now().year, datetime.now().month, datetime.now().day)):
		if date >= self.advent and date < self.christmas:
			return 'Advent'
		elif date >= self.christmas and date <= self.octave_of_epiphany:
			return 'Chrastmastide'
		elif date > self.octave_of_epiphany and date < self.septuagesima:
			return 'Ordinary Time'
		elif date >= self.septuagesima and date < self.ash_wed:
			return 'Septuagesima'
		elif date == self.easter- timedelta(days=3):
			return 'Holy Thursday'
		elif date == self.easter - timedelta(days=2):
			return 'Good Friday'
		elif date == self.easter - timedelta(days=1):
			return 'Holy Saturday'
		elif date == self.easter:
			return 'Easter Sunday'
		elif date >= self.easter - timedelta(days=6) and date < self.easter:
			return 'Holy Week'
		elif date >= self.ash_wed and date < self.easter:
			return 'Paschaltide'
		elif date >= self.easter and date < self.pentecost: 
			return 'Eastertide'
		elif date >= self.pentecost and date < self.advent:
			return 'Ordinary Time'



class RomanCalendar1970(RomanCalendar):

	def __init__(self,year=datetime.now().year):
		RomanCalendar.__init__(year)
	


#EOF
