import git
import json
import os
import shutil

class MessengerBuilder(object):
	"""docstring for MessengerBuilder"""
	def __init__(self, filepath, zipout):
		super(MessengerBuilder, self).__init__()
		self.cwd = os.getcwd()
		self.tmp = os.path.join(self.cwd, 'tmp')
		self.i18n = os.path.join(self.tmp, 'bin', 'i18n', 'locales')
		self.api = os.path.join(self.tmp, 'api')
		self.filepath = filepath
		self.zipout = zipout

	def build(self):
		self.__cleanup()
		self.__file_to_json()
		self.__clone_repo()
		self.__write_dot_env()
		self.__build_i18n_en()
		self.__write_i18n_en()
		self.__write_json_to_template()
		
	def __build_i18n_en(self):
		"""
			read JSON, map to English outputs

			primary key
				- elements
					text, photo, web
				- options
					nav

				0) set configs
					- create .env file
					- set default routes
						
						fallback:
							in.js:79
								response = [
									API.genText(
									  i18n.__("fallback.any", {
									    message: message
									  })
									),
									API.genQuickReply(i18n.__("get_started.guidance"), [
									  {
									    title: i18n.__("menu.suggestion"),
									    payload: "MENU"
									  }
									])
								]

						
						greeting:
							primary navigation route: "MENU" or similar
							default home route


						welcome:
							in.js:144
								response = API.genQuickReply(welcomeMessage, [
							      {
							        title: i18n.__("menu.suggestion"),
							        payload: "MENU"
							      },
							      {
							        title: i18n.__("menu.help"),
							        payload: "SUPPORT_HELP"
							      }
							    ])

				1) needs switch on navigations file
				case "PRODUCTS_DEODORANTS":
				response = products("DEODORANTS")
				break;

				2) switch needs instructions
					text: 
						API.genText(i18n.__("products.unispecies")),

					photo: 
						API.genImageTemplate(
						  images[media],
						  i18n.__(`media.${media}.title`),
						  i18n.__(`media.${media}.subtitle`)
						)

					web:
				        API.genGenericTemplate(
				          `https://storage.needpix.com/rsynced_images/buy-now-2541975_1280.png`,
				          i18n.__("menu.title"),
				          i18n.__("menu.subtitle"),
				          API.genWebButton()
				        )

					nav:
						API.genQuickReply(i18n.__("order.prompt"), [
				          {
				            title: i18n.__("order.account"),
				            payload: "LINK_ORDER"
				          },
				          {
				            title: i18n.__("order.search"),
				            payload: "SEARCH_ORDER"
				          },
				          {
				            title: i18n.__("menu.help"),
				            payload: "SUPPORT_ORDER"
				          }
				        ])

		"""
		self.i18n_en = {}
		views = self.data['views']
		for view in views:
			elements = self.data['views'][view]['elements']
			options = self.data['views'][view]['options']
			for i, element in enumerate(elements):
				key = '{}-{}-{}-{}'.format(
					view, 'elements', i, element['type']
					)
				if element['type'] == 'text':
					# text
					val = element['value']
					self.i18n_en[key] = val
				else:
					# photo / web
					val = element['value']
					if 'title' in val:
						_key = '{}-{}'.format(
							key, 'title')
						_val = val['title']
						self.i18n_en[_key] = _val
					if 'subtitle' in val:
						_key = '{}-{}'.format(
							key, 'subtitle')
						_val = val['subtitle']
						self.i18n_en[_key] = _val

			for i, option in enumerate(options):
				key = '{}-{}-{}-{}'.format(
					view, 'options', i, element['type'])
				if element['type'] == 'nav':
					self.i18n_en[key] = option['value']['text']

		self.__write_i18n_en()

	def __chdir_api(self):
		"""cd api dir"""
		os.chdir(self.api)

	def __chdir_i18n(self):
		"""cd i18n dir"""
		os.chdir(self.i18n)

	def __chdir_tmp(self):
		"""cd repo dir"""
		os.chdir(self.tmp)

	def __chdir_usr(self):
		"""cd main dir"""
		os.chdir(self.cwd)

	def __cleanup(self):
		"""delete skeleton & make empty dir"""
		shutil.rmtree(self.tmp, ignore_errors=True, onerror=None)
		os.mkdir(self.tmp)

	def __clone_repo(self):
		"""pull project skeleton"""
		repo = git.Repo.clone_from(
		    'https://github.com/Cologne-Dog/messenger-commerce-bot.git',
		    './tmp',
		    branch='builder'
		)

	def __file_to_json(self):
		"""read file, set JSON"""
		with open(self.filepath) as json_file:
			self.data = json.load(json_file)

	def __write_dot_env(self):
		"""app configurations for deployment"""
		self.__chdir_tmp()
		f = open('.env', 'x')
		f.write('APP_ID=%s\n' % self.data['configs']['appId'])
		f.write('PAGE_ID=%s\n' % self.data['configs']['pageId'])
		f.write('PAGE_ACCESS_TOKEN=%s\n' % self.data['configs']['pageToken'])
		f.write('APP_SECRET=%s\n' % self.data['configs']['secret'])
		f.write('VERIFY_TOKEN=%s\n' % self.data['configs']['verifyToken'])
		f.write('APP_URL=%s\n' % 'https://foo.com')
		f.write('SHOP_URL=%s\n' % self.data['configs']['webURL'])
		f.write('PORT=%s\n' % 3000)
		f.close()

	def __write_i18n_en(self):
		"""defaults to US English only"""
		self.__chdir_i18n()
		filename = 'en_US.json'
		f = open(filename, 'w')
		f.write(json.dumps(self.i18n_en, indent=4))
		f.close()

	def __write_json_to_template(self):
		"""input JSON to template for dynamic rendering"""
		self.__chdir_api()
		f = open('api.json', 'x')
		f.write(json.dumps(self.data['views'], indent=4))
		f.close()
