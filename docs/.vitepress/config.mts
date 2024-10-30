import { defineConfig } from 'vitepress'

export default defineConfig({
  lang: "zh_CN",
  title: "d3dxSkinManage",
  description: "3dmigoto skin mods manage tool",
  lastUpdated: true,

  head: [
    ['link', { rel: 'icon', href: '/static/favicon.png' }]
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
      "/changelog/": [
        {
          text: '计划更新日志',
          items: [
            { text: '计划更新内容', link: '/changelog/planned' }
          ]
        },
        {
          text: '简略更新日志',
          items: [
            { text: 'v1.6.x', link: '/changelog/simple/106xx' },
            { text: 'v1.5.x', link: '/changelog/simple/105xx' },
            { text: 'v1.4.x', link: '/changelog/simple/104xx' },
            { text: 'v1.3.x', link: '/changelog/simple/103xx' },
            { text: 'v1.2.x', link: '/changelog/simple/102xx' },
            { text: 'v1.1.x', link: '/changelog/simple/101xx' }
          ]
        },
        {
          text: '详细更新日志',
          items: [
            { text: 'v1.6.1', link: '/changelog/detail/10601' },
            { text: 'v1.6.0', link: '/changelog/detail/10600' },
            { text: 'v1.5.38', link: '/changelog/detail/10538' },
            { text: 'v1.5.37', link: '/changelog/detail/10537' },
            { text: 'v1.5.36', link: '/changelog/detail/10536' }
          ]
        }
      ],
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
                { text: '头像缩略图', link: '/help/tutorial-thumbnail' },
                { text: '筛选功能', link: '/help/tutorial-search' },
                { text: '全局设置', link: '/help/tutorial-global-settings' },
                { text: '补充内容', link: '/help/tutorial-supplement' }
              ]
            },
            {
              text: '扩展功能',
              link: '/help/tutorial-extensions',
              items: [
                { text: 'Mods 仓库', link: '/help/tutorial-mods-warehouse' },
                { text: '强迫症截图工具', link: '/help/tutorial-ocdcrop' },
                // { text: '缓存清理工具', link: '/help/' },
                // { text: '旧版MOd管理器数据迁移工具', link: '/help/' },
                // { text: '可选标签编辑工具', link: '/help/' },
                { text: '插件', link: '/help/tutorial-plugins' }
              ]
            },
            {
              text: '反和谐使用教程',
              link: '/help/oppose-harmony',
            }
          ]
        },
        {
          text: '帮助',
          items: [
            { text: '常见问题', link: '/help/faqs' },
            { text: 'v1.6.x 兼容问题', link: '/help/compatibility-16' },
            { text: '更新时遇到问题', link: '/help/update-problem' },
            { text: '禁用更新检查', link: '/help/disable-update-check' },
            { text: '关于管理员权限', link: '/help/about-admin-rights' },
            
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
            { text: '扩展插件', link: '/resources/plugins' },
            { text: '缩略图资源', link: '/resources/thumbnail' },
            { text: '3DMiGoto 加载器', link: '/resources/3dmigoto' },
            { text: '模组资源', link: '/resources/modules' }
          ]
        },
        {
          text: '插件',
          items: [
            { text: 'gi_update_mods', link: '/resources/plugins/gi_update_mods' },
            { text: 'sr_update_mods', link: '/resources/plugins/sr_update_mods' },
            { text: 'zzz_update_mods', link: '/resources/plugins/zzz_update_mods' },
            { text: 'ww_update_mods', link: '/resources/plugins/ww_update_mods' },
            { text: 'enforcelogout', link: '/resources/plugins/enforcelogout' },
            { text: 'dropfiles_multiple', link: '/resources/plugins/dropfiles_multiple' },
            { text: 'batch_processing_tools', link: '/resources/plugins/batch_processing_tools' },
            { text: 'multiple_preview', link: '/resources/plugins/multiple_preview' },
            { text: 'modify_list_order', link: '/resources/plugins/modify_list_order' },
            { text: 'modify_key_swap', link: '/resources/plugins/modify_key_swap' },
            { text: 'modify_3dm_swap', link: '/resources/plugins/modify_3dm_swap' },
            { text: 'modify_object_name', link: '/resources/plugins/modify_object_name' },
            { text: 'auto_login', link: '/resources/plugins/auto_login' },
            { text: 'auto_reload_mods', link: '/resources/plugins/auto_reload_mods' },
            { text: 'handle_user_env', link: '/resources/plugins/handle_user_env' },
            { text: 'enable_mods_warehouse', link: '/resources/plugins/enable_mods_warehouse' },
            { text: 'delete_and_remove_mod', link: '/resources/plugins/delete_and_remove_mod' },
            { text: 'delete_mod_cache', link: '/resources/plugins/delete_mod_cache' },
            { text: 'delete_index_no_file', link: '/resources/plugins/delete_index_no_file' },
            { text: 'get_GI_images', link: '/resources/plugins/get_GI_images' },
            { text: 'get_SR_images', link: '/resources/plugins/get_SR_images' },
            { text: 'get_ZZZ_images', link: '/resources/plugins/get_ZZZ_images' },
            { text: 'get_WW_images', link: '/resources/plugins/get_WW_images' },
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
      pattern: 'https://github.com/numlinka/d3dxSkinManage/edit/master/docs/:path',
      text: '在 GitHub 上编辑此页面'
    },

    docFooter: {
      prev: '上一页',
      next: '下一页'
    },
  }
})
