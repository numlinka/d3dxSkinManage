---
layout: page
sidebar: false
---

<script setup>
import {
  VPTeamPage,
  VPTeamPageTitle,
  VPTeamMembers
} from 'vitepress/theme'

const members = [
  {
    avatar: 'static/avatars/numlinka.jpg',
    name: 'numlinka',
    title: '项目创建',
    desc: '',
    links: [
      { icon: 'github', link: 'https://github.com/numlinka' },
      { icon: 'gitee', link: 'https://gitee.com/numlinka' },
      { icon: 'afdian', link: 'https://afdian.com/a/numlinka' }
    ],
    sponsor: 'https://afdian.com/a/numlinka',
    actionText: '成为赞助者'
  },
  {
    avatar: 'static/avatars/ticca.jpg',
    name: '黎愔',
    title: '插件开发 页面编辑',
    desc: '',
    links: [
      { icon: 'github', link: 'https://github.com/Ticca-Liyin' },
      { icon: 'gitee', link: 'https://gitee.com/ticca' },
      { icon: 'bilibili', link: 'https://space.bilibili.com/1397930555' },
      { icon: 'afdian', link: 'https://afdian.com/a/ticca' }
    ],
    sponsor: 'https://afdian.com/a/ticca',
    actionText: '成为赞助者'
  },
]
</script>

<VPTeamPage>
  <VPTeamPageTitle>
    <template #title>项目贡献</template>
    <template #lead>我们欢迎任何形式的贡献，其中一些成员选择在下面展示</template>
  </VPTeamPageTitle>
  <VPTeamMembers :members="members" />
</VPTeamPage>
