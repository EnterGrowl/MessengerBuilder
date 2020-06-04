import git
import json
import os
import shutil

class MessengerBuilder(object):
    """docstring for MessengerBuilder"""
    def __init__(self, _json, port):
        super(MessengerBuilder, self).__init__()
        self.data = _json
        self.port = port
        self.cwd = os.getcwd()
        self.tmp = os.path.join(self.cwd, 'store', port)
        print('self.tmp', self.tmp)
        self.i18n = os.path.join(self.tmp, 'bin', 'i18n', 'locales')
        self.api = os.path.join(self.tmp, 'api')
        self.defaults = os.path.join(self.tmp, 'bin', 'io', 'in.js')
        self.render = os.path.join(self.tmp, 'bin', 'io', 'render.js')

    def build(self):
        try:
            self.__cleanup()
            # self.__file_to_json()
            self.__clone_repo()
            self.__write_dot_env()
            self.__build_i18n_en()
            self.__write_i18n_en()
            self.__write_json_to_template()
            defaults = ['greeting', 'fallback', 'welcome']
            for default in defaults:
                self.__template_default(default)
            return 0
        except Exception as e:
            print(e)
            return 1

    def __build_i18n_en(self):
        """generate all template text in i18n"""
        self.i18n_en = {}
        views = self.data['views']
        for view in views:
            elements = self.data['views'][view]['elements']
            options = self.data['views'][view]['options']
            self.i18n_en.update(self.__names_and_text_from_JSON(view, elements))
            self.i18n_en.update(self.__names_and_text_from_JSON(view, options, True))

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
            self.tmp,
            branch='builder'
        )

    def __file_to_json(self):
        """read file, set JSON"""
        with open(self.filepath) as json_file:
            self.data = json.load(json_file)

    def __names_and_text_from_JSON(self, view, elements, is_option=False):
        agg = {'nav': 'Please select an option:'}
        for i, element in enumerate(elements):
            if is_option:
                key = '{}-{}-{}-{}'.format(
                    view, 'options', i, element['type'])
                if element['type'] == 'nav':
                    agg[key] = element['value']['text']
            else:
                key = '{}-{}-{}-{}'.format(
                    view, 'elements', i, element['type']
                    )
                if element['type'] == 'text':
                    # text
                    val = element['value']
                    agg[key] = val
                else:
                    # photo / web
                    val = element['value']
                    if 'title' in val:
                        _key = '{}-{}'.format(
                            key, 'title')
                        _val = val['title']
                        agg[_key] = _val
                    if 'subtitle' in val:
                        _key = '{}-{}'.format(
                            key, 'subtitle')
                        _val = val['subtitle']
                        agg[_key] = _val
        return agg

    def __template_default(self, name):
        delimiter = '%%{}%%'.format(name)
        view = self.data['views'][name]
        elements = view['elements']
        options = view['options']
        res = """
    let response = [
        """
        res += self.__template_elements(elements, name)
        res += self.__template_options(options, name)
        res += """
    ]
        """
        with open(self.defaults, 'r') as file:
            data = file.read().replace(delimiter, res)
            os.remove(self.defaults)
            f = open(self.defaults, 'w')
            f.write(data)
            f.close()


    def __template_elements(self, views, name):
        res = ''
        for i, view in enumerate(views):
            key = '{}-{}-{}-{}'.format(
                name, 'elements', i, view['type']
                )
            if view['type'] == 'text':
                res += """
        API.genText(
            i18n.__("{}")
        ),
                """.format(self.i18n_en[key])
            else:
                title = '{}-{}'.format(key, 'title')
                subtitle = '{}-{}'.format(key, 'subtitle')
                if view['type'] == 'photo':
                    res += """
        API.genImageTemplate(
            "{}",
            i18n.__("{}"),
            i18n.__("{}")
        ),
                    """.format(
                        view['value']['image'],
                        title,
                        subtitle)
                elif view['type'] == 'web':
                    res += """
        API.genGenericTemplate(
          "{}",
          i18n.__("{}"),
          i18n.__("{}"),
          API.genWebButton({})
        ),
                    """.format(
                        view['value']['image'],
                        title,
                        subtitle,
                        view['value']['url'])

        return res

    def __template_options(self, routes, name):
        if len(routes) == 0:
            return ''
        
        res = """
        this.genQuickReply(i18n.__("nav"), [
        """
        for i, route in enumerate(routes):
            key = '{}-{}-{}-{}'.format(
                name, 'options', i, route['type'])

            res += """
            {
            """
            res += """
                title: i18n.__("{}"), payload: "{}"
            """.format(
                key, route['value']['destination'])
            res += """
            },
            """
        
        res += """
        ])
        """
        return res


    def __write_dot_env(self):
        """app configurations for deployment"""
        self.__chdir_tmp()
        f = open('.env', 'x')
        f.write('APP_ID=%s\n' % self.data['configs']['appId'])
        f.write('PAGE_ID=%s\n' % self.data['configs']['pageId'])
        f.write('PAGE_ACCESS_TOKEN=%s\n' % self.data['configs']['pageToken'])
        f.write('APP_SECRET=%s\n' % self.data['configs']['secret'])
        f.write('VERIFY_TOKEN=%s\n' % self.data['configs']['verifyToken'])
        f.write('WEB_URLS="%s"\n' % ','.join(self.data['configs']['webURLs']))
        f.write('APP_URL=https://%s.messengerup.com\n' % self.port)
        f.write('PORT=%s\n' % self.port)
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
