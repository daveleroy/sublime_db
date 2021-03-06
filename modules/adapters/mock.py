import os
from ..typecheck import *
from .import adapter

class Mock(adapter.AdapterConfiguration):

	type = 'mock'
	docs = 'https://github.com/microsoft/vscode-mock-debug#vs-code-mock-debug'

	@property
	def info(self): return adapter.vscode.info(self.type)

	async def start(self, log, configuration):
		node = await adapter.get_and_warn_require_node(self.type, log)
		install_path = adapter.vscode.install_path(self.type)
		command = [
			node,
			f'{install_path}/extension/out/debugAdapter.js'
		]
		return adapter.StdioTransport(log, command)

	async def install(self, log):
		url = 'https://github.com/microsoft/vscode-mock-debug/archive/master.zip'

		async def post_download_action():
			install_path = adapter.vscode.install_path(self.type)
			
			original_folder = os.path.join(install_path, 'vscode-mock-debug-master')
			extension_folder = os.path.join(install_path, 'extension')
			
			# rename the folder so it matches the vscode convention
			# since the adapter.vscode code assumes this
			os.rename(original_folder, extension_folder)

			log.info('building mock debug adapter')
			log.info('npm install')
			await adapter.Process.check_output(['npm', 'install'], cwd=extension_folder)
			log.info('npm run compile')
			await adapter.Process.check_output(['npm', 'run', 'compile'], cwd=extension_folder)

		await adapter.vscode.install(self.type, url, log, post_download_action)
		

	@property
	def installed_version(self) -> Optional[str]:
		return adapter.vscode.installed_version(self.type)

	@property
	def configuration_snippets(self) -> Optional[list]:
		return adapter.vscode.configuration_snippets(self.type)

	@property
	def configuration_schema(self) -> Optional[dict]:
		return adapter.vscode.configuration_schema(self.type)
