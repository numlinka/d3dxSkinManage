import { defineConfig } from 'vitepress'

export default defineConfig({
  base: "/d3dxSkinManage/",

  lang: "zh_CN",
  title: "d3dxSkinManage",
  description: "3dmigoto skin mods manage tool",
  lastUpdated: true,

  head: [
    ['link', { rel: 'icon', href: '/d3dxSkinManage/static/favicon.png' }]
  ],

  themeConfig: {
    logo: "/static/favicon.png",
    outline: [2, 3],
    outlineTitle: "页面导航",
    lastUpdatedText: "最后更新于",

    nav: [
      { text: '主页', link: '/' },
      { text: '帮助', link: '/help' },
      { text: '文档', link: '/docs' },
      { text: '资源下载', link: '/resources' },
      { text: '更新日志', link: '/changelog' },
      { text: '项目贡献', link: '/contribution' }
    ],

    sidebar: {
      "/": [],
      "/docs/": [
        {
          text: '文档',
          items: [
            { text: '目录结构', link: '/docs/directory-structure' },
            { text: '模组索引文件', link: '/docs/mods-index' },
            { text: '缩略图配置文件', link: '/docs/config-redirection' },
            { text: '加载器行为文件', link: '/docs/config-scheme' }
          ]
        }
      ],
      "/help/": [
        {
          text: '教程',
          items: [
            {
              text: '快速上手',
              link: '/help/tutorial',
              items: [
                { text: '下载和安装', link: '/help/tutorial-install' },
                { text: '用户环境', link: '/help/tutorial-userenv' },
                { text: '配置加载器', link: '/help/tutorial-loader' },
                { text: '管理模组', link: '/help/tutorial-modules' },
                { text: '对象分类', link: '/help/tutorial-classify' },
                { text: '头像缩略图', link: '/help/tutorial-thumbnail' }
              ]
            }
          ]
        },
        {
          text: '帮助',
          items: [
            { text: '更新时遇到问题', link: '/help/update-problem' },
            { text: '禁用更新检查', link: '/help/disable-update-check' }
          ]
        },
        { text: '项目社区', link: '/help/community' },
        { text: '其它项目推荐', link: '/help/others' }
      ],
      "/resources/": [
        {
          text: '资源下载',
          items: [
            { text: 'd3dxSkinManage', link: '/resources/download' },
            { text: '更新组件', link: '/resources/update' },
            { text: '插件', link: '/resources/plugins' },
            { text: '缩略图资源', link: '/resources/thumbnail' },
            { text: '3DMiGoto 加载器', link: '/resources/3dmigoto' },
            { text: '皮肤模组', link: '/resources/modules' }
          ]
        }
      ],
    },

    socialLinks: [
      { icon: 'github', link: 'https://github.com/numlinka/d3dxSkinManage' }
    ],

    footer: {
      message: 'Licensed under the GNU General Public License v3.0',
      copyright: 'Copyright © 2023 numlinka'
    },

    editLink: {
      pattern: 'https://github.com/numlinka/d3dxskin-managedocs/edit/master/:path',
      text: '在 GitHub 上编辑此页面'
    },

    docFooter: {
      prev: '上一页',
      next: '下一页'
    },
  }
})
